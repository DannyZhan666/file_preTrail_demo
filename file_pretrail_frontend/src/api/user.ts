import myAxios from "@/request";

export const userRegister = async (params: any) => {
  return await myAxios.request({
    url: "/user/register",
    method: "POST",
    data: params,
  });
};

/**
 * 用户登录
 * @param params
 */
export const userLogin = async (params: any) => {
  return myAxios.request({
    url: "/user/login",
    method: "POST",
    data: params,
  });
};

export const getCurrentUser = async () => {
  // 从 sessionStorage 获取存储的 JWT Token
  const token = sessionStorage.getItem("token");
  console.log(token);

  // 返回请求，携带 Authorization Header
  return myAxios.request({
    url: "/user/current",  // 路径保持不变
    method: "GET",
    headers: {
      'Authorization': token ? `Bearer ${token}` : '',  // 如果 Token 存在，则添加 Authorization Header
    },
  });
};

export const updateUserInfo = async (params: any) => {
  return await myAxios.request({
    url: "/user/update",
    method: "POST",
    data: params,
  });
};

export const userLogout = async () => {
  // 通知后端使 JWT 失效（可选）
  try {
    await myAxios.request({
      url: "/user/logout",
      method: "POST",
    });
  } catch (error) {
    console.error("登出请求失败", error);
  }

  // 清除客户端存储的 JWT
  sessionStorage.removeItem("token");
};

export const jobCreate = async (params: any) => {
  return myAxios.request({
    url: "/job/create",
    method: "POST",
    data: params,
  });
};

export const fileUpload = async (params: any) => {
  return myAxios.request({
    url: "/file/upload",
    method: "POST",
    data:params,
    headers: {
        "Content-Type": "multipart/form-data",
    }
  });
};

