import { spawn, SpawnOptionsWithoutStdio } from "child_process";

export function call(
  command: string,
  args?: ReadonlyArray<string>,
  options?: SpawnOptionsWithoutStdio
): Promise<{
  code: number | null;
  signal: NodeJS.Signals | null;
  str: string;
}> {
  return new Promise((resolve, reject) => {
    try {
      let process = spawn(command, args, options);
      let str = "";
      process.stdout.on("data", data => {
        str += data;
      });
      process.on("close", (code, signal) => {
        resolve({ code, signal, str });
      });
      process.on("error", err => {
        reject(err);
      });
    } catch (err) {
      reject(err);
    }
  });
}
