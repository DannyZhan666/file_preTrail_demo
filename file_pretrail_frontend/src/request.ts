import axios from "axios";

const myAxios = axios.create({
  baseURL: "http://localhost:8000",
  timeout: 100000,
  withCredentials: true,
});

// // 添加请求拦截器
// axios.interceptors.request.use(
//   function (config) {
//     // 在发送请求之前做些什么
//     return config;
//   },
//   function (error) {
//     // 对请求错误做些什么
//     return Promise.reject(error);
//   }
// );
//
// // 添加响应拦截器
// axios.interceptors.response.use(
//   function (response) {
//     // 对响应数据做点什么
//     console.log(response);
//     const { data } = response;
//     console.log(data);
//     // 未登录
//     if (data.code === 40100) {
//       // 不是获取用户信息接口，或者不是登录页面，则跳转至登录页面
//       if (
//         !response.request.responseURL.incudes("/user/current") &&
//         !window.location.pathname.includes("/user/login")
//       ) {
//         window.location.href = `/user/login?redirect=${window.location.href}`;
//       }
//     }
//     return response;
//   },
//   function (error) {
//     // 对响应错误做点什么
//     return Promise.reject(error);
//   }
// );

// 在请求前添加拦截器，自动带上 Token
myAxios.interceptors.request.use(config => {
    const token = sessionStorage.getItem("token");  // 从 sessionStorage 中获取 Token
    if (token) {
        console.log("JWT Token:", token);  // 打印 Token，检查是否成功读取
        config.headers['Authorization'] = `Bearer ${token}`;  // 自动将 Token 放入请求头
    } else {
        console.log("Token not found in sessionStorage");  // 如果 Token 没找到，打印此信息
    }
    return config;
}, error => {
    return Promise.reject(error);
});

export default myAxios;
