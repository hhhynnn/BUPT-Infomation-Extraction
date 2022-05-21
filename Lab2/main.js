"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const koa_1 = __importDefault(require("koa"));
const koa_router_1 = __importDefault(require("koa-router"));
const koa_static_1 = __importDefault(require("koa-static"));
const path_1 = __importDefault(require("path"));
const app = new koa_1.default();
const router = new koa_router_1.default();
router.redirect("/", "/index.html");
app.use(router.routes()).use((0, koa_static_1.default)(path_1.default.join(__dirname, "app/build")));
router.get("/api/search", (ctx) => __awaiter(void 0, void 0, void 0, function* () {
    const keyword = ctx.query.q;
    console.log(keyword);
    ctx.response.body = `查找关键词：${keyword}`;
}));
app.listen(8080);
console.log("http://localhost:8080/");
