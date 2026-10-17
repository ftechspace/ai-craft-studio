// FilmCraft control-channel client (JSON lines on 127.0.0.1:9876; start the app with --control 9876).
//
// CLI:
//   node tools/fc.js <command> ['<json params>']      engine command, prints the result
//   node tools/fc.js --ui <method> ['<json params>']  raw control method (ui.screenshot, ui.set, ui.inspect, …)
//   node tools/fc.js --run <script.jsonl> [--keep-going]   one {"id","params"} per line, then file.save
//   node tools/fc.js --wait                           wait until no export/render job is running
// Module:
//   const fc = await require("./fc").connect(); await fc.cmd(id, params); await fc.call(method, params);
//   await fc.waitJobs(); fc.close();
//   connectHeadless(project?) gives the same cmd/waitJobs/close on a hidden session (filmcraft-cli mcp), no UI —
//   for dry runs and tests that must not touch the user's open app. fc.headless is true there.
const net = require("net");
const path = require("path");

function connectHeadless(project) {
  const { spawn } = require("child_process");
  const exe = process.env.FILMCRAFT_CLI || path.join(__dirname, "..", "apps", "filmcraft", "target", "release", "filmcraft-cli.exe");
  const p = spawn(exe, ["mcp", ...(project ? ["--project", project] : [])], { stdio: ["pipe", "pipe", "ignore"] });
  const waiting = new Map();
  let buf = "", next = 1;
  p.stdout.on("data", d => {
    buf += d;
    for (let i; (i = buf.indexOf("\n")) >= 0; buf = buf.slice(i + 1)) {
      const m = JSON.parse(buf.slice(0, i));
      waiting.get(m.id)?.(m);
      waiting.delete(m.id);
    }
  });
  const rpc = (method, params) => new Promise(res => { const id = next++; waiting.set(id, res); p.stdin.write(JSON.stringify({ jsonrpc: "2.0", id, method, params }) + "\n"); });
  const cmd = async (command, params = {}) => {
    const m = await rpc("tools/call", { name: "command_run", arguments: { id: command, params } });
    const text = m.result?.content?.[0]?.text ?? m.error?.message ?? "";
    if (m.error || m.result?.isError) throw new Error(`${command}: ${text}`);
    try { return JSON.parse(text); } catch { return text; }
  };
  const call = async method => { throw new Error(`${method} needs the live app (headless session)`); };
  const waitJobs = async () => {
    for (;;) { if (!(await cmd("jobs.list")).some(j => !j.finished)) return; await new Promise(r => setTimeout(r, 2000)); }
  };
  return rpc("initialize", { protocolVersion: "2025-06-18", capabilities: {}, clientInfo: { name: "fc.js", version: "1" } }).then(() => {
    p.stdin.write(JSON.stringify({ jsonrpc: "2.0", method: "notifications/initialized" }) + "\n");
    return { call, cmd, waitJobs, headless: true, close: () => { p.stdin.end(); p.kill(); } };
  });
}

function connect(port = Number(process.env.FILMCRAFT_PORT || 9876)) {
  return new Promise((resolve, reject) => {
    const sock = net.connect(port, "127.0.0.1");
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
    sock.on("error", e => reject(new Error(`FilmCraft isn't reachable on port ${port} (start it with start-filmcraft.cmd): ${e.message}`)));
    const call = (method, params = {}) => new Promise((res, rej) => {
      const id = next++;
      waiting.set(id, m => (m.ok ? res(m.result) : rej(new Error(`${method === "engine.execute" ? params.command : method}: ${m.error}`))));
      sock.write(JSON.stringify({ id, method, params }) + "\n");
    });
    const cmd = (command, params = {}) => call("engine.execute", { command, params });
    const waitJobs = async (ms = 5000) => {
      for (;;) {
        const running = (await cmd("jobs.list")).filter(j => !j.finished);
        if (!running.length) return;
        await new Promise(r => setTimeout(r, ms));
      }
    };
    sock.on("connect", () => resolve({ call, cmd, waitJobs, close: () => sock.end() }));
  });
}
module.exports = { connect, connectHeadless, TPS: 254016000000 };

if (require.main === module) {
  (async () => {
    const a = process.argv.slice(2);
    const fc = await connect();
    const json = s => (s ? JSON.parse(s) : {});
    if (a[0] === "--ui") console.log(JSON.stringify(await fc.call(a[1], json(a[2]))));
    else if (a[0] === "--wait") await fc.waitJobs();
    else if (a[0] === "--run") {
      const lines = require("fs").readFileSync(a[1], "utf8").split("\n").filter(l => l.trim() && !l.trim().startsWith("#"));
      let failed = 0;
      for (const l of lines) {
        const { id, params } = JSON.parse(l);
        await fc.cmd(id, params).catch(e => { failed++; console.log(e.message); if (!a.includes("--keep-going")) throw e; });
      }
      await fc.cmd("file.save");
      console.log(`${lines.length} commands, ${failed} failed, saved`);
    } else console.log(JSON.stringify(await fc.cmd(a[0], json(a[1])), null, 1));
    fc.close();
  })().catch(e => { console.error(e.message); process.exit(1); });
}
