import { defineStore } from "pinia";
import { ref } from "vue";
import { getCurrentUser,userLogout } from "@/api/user";

export const useLoginUserStore = defineStore("useLoginUser", () => {
  const loginUser = ref<any>({
    username: "未登录",
    userRole: -1,
  });

  // 单独设置信息
  async function fetchLoginUser() {
    const res = await getCurrentUser();
    if (res.data.code === 200 && res.data.data) {
      loginUser.value = res.data.data;
    } else if(res.data.code === 200 && !res.data.data) {
      setTimeout(() => {
        loginUser.value = { username: "小黑子"};
      }, 2000);
    }
  }

  function setLoginUser(newLoginUser: any) {
    loginUser.value = newLoginUser;
  }

  async function logout() {
    const res = await userLogout();
    loginUser.value = { username: "", userRole: -1 };
  }

  return { loginUser, fetchLoginUser, setLoginUser, logout };
});
