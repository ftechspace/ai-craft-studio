// One control-channel client for every Craft app (JSON lines on 127.0.0.1:<port>, same protocol as tools/fc.js).
//
//   node tools/craft.js <app> --start [args…]            launch the app (release build) with its control port open
//   node tools/craft.js <app> <command> ['<json params>'] engine command, prints the result
//   node tools/craft.js <app> --ui <method> ['<json>']    raw control method (ui.screenshot, ui.inspect, doc.open, …)
//   node tools/craft.js <app> --run <script.jsonl>        one {"id","params"} per line
//   node tools/craft.js ports                             list apps and ports
// Module: const app = await require("./craft").connect("soundcraft"); await app.cmd(id, params); app.close();
// Per-app commands, CLI/headless use and pitfalls: editor-kb/<app>-operations.md.
const net = require("net");
const path = require("path");

const PORTS = { photocraft: 9871, lightcraft: 9872, soundcraft: 9873, vectorcraft: 9874, effectcraft: 9875, filmcraft: 9876, designcraft: 9877 };
const ROOT = path.join(__dirname, "..");
const exe = (app, cli) => path.join(ROOT, "apps", app, "target", "release", `${app}${cli ? "-cli" : ""}.exe`);

function port(app) {
  if (!PORTS[app]) throw new Error(`unknown app "${app}" (${Object.keys(PORTS).join(", ")})`);
  return Number(process.env[`${app.toUpperCase()}_PORT`] || PORTS[app]);
}

// PhotoCraft's channel is authenticated and sandboxed to file roots; the others need nothing extra.
const PHOTOCRAFT_TOKEN = path.join(process.env.APPDATA || "", "Photocraft", "control.token");
const EXTRA = {
  photocraft: ["--control-token-file", PHOTOCRAFT_TOKEN, "--automation-read-root", ROOT, "--automation-write-root", path.join(ROOT, "projects")],
};

function start(app, args = []) {
  const { spawn } = require("child_process");
  spawn(exe(app), [...args, ...(EXTRA[app] || []), "--control", String(port(app))], { detached: true, stdio: "ignore", cwd: ROOT }).unref();
}

function connect(app) {
  const p = port(app);
  return new Promise((resolve, reject) => {
    const sock = net.connect(p, "127.0.0.1");
    const waiting = new Map();
    let buf = "", next = 1;
    sock.on("data", d => {
      buf += d;
      for (let i; (i = buf.indexOf("\n")) >= 0; buf = buf.slice(i + 1)) {
        const m = JSON.parse(buf.slice(0, i));
        waiting.get(m.id)?.(m);
        waiting.delete(m.id);
      }
    });
    sock.on("error", e => reject(new Error(`${app} isn't reachable on port ${p} (node tools/craft.js ${app} --start): ${e.message}`)));
    const call = (method, params = {}) => new Promise((res, rej) => {
      const id = next++;
      waiting.set(id, m => (m.ok !== false && !m.error ? res(m.result) : rej(new Error(`${method === "engine.execute" ? params.command : method}: ${JSON.stringify(m.error)}`))));
      sock.write(JSON.stringify({ id, method, params }) + "\n");
    });
    const cmd = (command, params = {}) => call("engine.execute", { command, params });
    sock.on("connect", async () => {
      try {
        if (app === "photocraft") await call("auth", { token: require("fs").readFileSync(PHOTOCRAFT_TOKEN, "utf8").trim() });
        resolve({ call, cmd, close: () => sock.end() });
      } catch (e) { reject(e); }
    });
  });
}
module.exports = { connect, start, exe, PORTS };

if (require.main === module) {
  (async () => {
    const [app, ...a] = process.argv.slice(2);
    if (app === "ports" || !app) return console.log(PORTS);
    if (a[0] === "--start") return start(app, a.slice(1));
    const c = await connect(app);
    const json = s => (s ? JSON.parse(s) : {});
    if (a[0] === "--ui") console.log(JSON.stringify(await c.call(a[1], json(a[2])), null, 1));
    else if (a[0] === "--run") {
      const lines = require("fs").readFileSync(a[1], "utf8").split("\n").filter(l => l.trim() && !l.trim().startsWith("#"));
      for (const l of lines) { const { id, params } = JSON.parse(l); await c.cmd(id, params); }
      console.log(`${lines.length} commands ok`);
    } else console.log(JSON.stringify(await c.cmd(a[0], json(a[1])), null, 1));
    c.close();
  })().catch(e => { console.error(e.message); process.exit(1); });
}
