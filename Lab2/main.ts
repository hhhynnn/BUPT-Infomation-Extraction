import { call } from "./utils";
import Koa from "koa";
import Router from "koa-router";
import staticResource from "koa-static";
import path from "path";

const app = new Koa();
const router = new Router();

router.redirect("/", "/index.html");

router.get("/api/search", async ctx => {
  const keyword = ctx.query.q as string;

  await call("python", ["search.py", "tfidf", keyword], {
    cwd: path.resolve(__dirname, "./api"),
  })
    .then(({ code, str }) => {
      console.log(
        `"python search.py tfidf ${keyword}" exited with code ${code}`
      );
      if (code !== 0) {
        return;
      }
      console.log(str.slice(0, 30) + " ..." + (str.length - 30) + " chars");
      ctx.response.body = `${str}`;
    })
    .catch(console.log);
});

app.use(router.routes());
app.use(staticResource(path.join(__dirname, "app/build")));

call("python", ["refresh_cache.py"], {
  cwd: path.resolve(__dirname, "./api"),
})
  .then(({ code }) => {
    console.log(`"python refresh_cache.py" exited with code ${code}`);
    if (code !== 0) {
      return;
    }
    app.listen(8080, () => {});
    console.log("http://localhost:8080/");
  })
  .catch(console.log);
