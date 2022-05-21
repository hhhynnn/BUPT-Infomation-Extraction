import Koa from "koa";
import Router from "koa-router";
import staticResource from "koa-static";
import path from "path";

const app = new Koa();
const router = new Router();

router.redirect("/", "/index.html");
app.use(router.routes()).use(staticResource(path.join(__dirname, "app/build")));

router.get("/api/search", async ctx => {
  const keyword = ctx.query.q;
  console.log(keyword);
  ctx.response.body = `查找关键词：${keyword}`;
});

app.listen(8080);

console.log("http://localhost:8080/");
