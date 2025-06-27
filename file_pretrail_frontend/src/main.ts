import {createApp} from "vue";
import App from "./App.vue";
import router from "./router";
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import axios from "axios";
import Antd from "ant-design-vue";
import "ant-design-vue/dist/reset.css";
import {createPinia} from "pinia";
import {myDoc} from "@/models/user";
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

const pinia = createPinia();

const app = createApp(App).use(pinia).use(Antd).use(router).use(ElementPlus);
// 注册 Element Plus 图标组件
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component);
}
app.mount("#app");

// axios 请求拦截器
// axios.interceptors.request.use(config => {
//     config.headers.Authorization = window.sessionStorage.getItem("token");
//     config.withCredentials = true;
//     return config;
// });

// 配置页面标题
router.afterEach(function (to, from) {
    if (to.meta.title) {
        const document: myDoc = {title: ""};
        document.title = to.meta.title as string;
    }
});

