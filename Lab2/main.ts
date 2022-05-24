import { spawn } from "child_process";
import Koa from "koa";
import Router from "koa-router";
import staticResource from "koa-static";
import path from "path";

const app = new Koa();
const router = new Router();

router.redirect("/", "/index.html");

router.get("/api/search", async ctx => {
  const keyword = ctx.query.q as string;
  console.log(keyword);
  const pythonProcess = spawn("python", ["api/test.py", keyword]);

  let data = "";
  for await (const chunk of pythonProcess.stdout) {
    console.log("stdout chunk: " + chunk);
    data += chunk;
  }

  ctx.response.body = `${keyword}: ${data}`;
});

app.use(router.routes());
app.use(staticResource(path.join(__dirname, "app/build")));

app.listen(8080, () => {
  console.log("http://localhost:8080/");
});
