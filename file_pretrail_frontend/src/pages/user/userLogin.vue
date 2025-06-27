<template>
  <div class="whole">
<!--    <img src="@/assets/imgs/grey_bg.jpeg" style="width: 1000px; height: 1000px;position: relative; top: 13px;right: 0px"/>-->
    <div class="login">
      <div class="title" style="color: #ff6a00">
        <img src="@/assets/imgs/title-logo.png" style="width: 50px;position: relative; top: -5px;right: 0px"/>
        <span style="font-size: 25px">文件预审系统</span>
      </div>
      <div class="my-form">
        <el-form :model="loginForm" status-icon size="small" label-position="top">
          <el-form-item label="账号" prop="account">
            <el-input
                type="text"
                v-model="loginForm.userAccount"
                :placeholder="'请输入'+labelMap.account">
              <template #prefix>
                <el-icon><User /></el-icon>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input
                type="password"
                v-model="loginForm.userPassword"
                autocomplete="off"
                :placeholder="'请输入'+labelMap.password">
              <template #prefix>
                <el-icon><Lock /></el-icon>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item class="btns">
            <el-button type="primary" @click="login()" style="width: 100%;">登 录</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {reactive, ref} from 'vue';
import {useRouter} from 'vue-router';
import {ElMessage} from 'element-plus';
import {userLogin} from "@/api/user";
import {useLoginUserStore} from "@/store/useLoginUserStore";

// 定义标签映射，用于占位符文本
const labelMap = {
  account: '账号',
  password: '密码'
};


const createDialogVisible = ref(false);
const addUser = reactive({
  userAccount: '',
  userPassword: '',
  checkPassword: '',
});

const loginForm = reactive({
  userAccount: 'ckc',
  userPassword: '12345678',
});

const router = useRouter();
const loginUserStore = useLoginUserStore();

const changePage = (path: string) => {
  router.push(path);
};

const login = async () => {
  const res = await userLogin(loginForm);
  const BaseResponse = res.data;
  const user = BaseResponse.data;
  // 登录成功，跳转到主页
  if (BaseResponse.code === 200) {
    // console.log(user);
    // 假设 BaseResponse.data 中包含了 JWT Token
    const token = BaseResponse.data.access_token;  // 确保后端返回了 token

    // 将 JWT Token 存储在 sessionStorage 或 localStorage 中
    sessionStorage.setItem("token", token);  // 或者使用 localStorage.setItem("token", token)
    await loginUserStore.fetchLoginUser();
    // message.success("登录成功");
    ElMessage({
      message: BaseResponse.msg,
      type: 'success',
    })
    if (user.userRole === 0) {
      // console.log("======" + user.userRole);
      router.push('/home');
    } else if (user.userRole === 1) {
      // console.log("------" + BaseResponse.data.userRole);
      router.push('/user');
    } else if (user.userRole === 2) {
      // console.log("++++++" + BaseResponse.data.userRole);
      router.push('/lawyer');
    } else {
      // console.log("%%%%%%%" + BaseResponse.data.userRole);
      router.push('/404');
    }
  } else {
    ElMessage({
      message: BaseResponse.msg,
      type: 'error',
    })
  }
};

const reset = () => {
  loginForm.userAccount = '';
  loginForm.userPassword = '';
  loginForm.role = 'user';
};
</script>


<style scoped>

.whole {
  width: 100%;
  height: 100%;
  background-image: url('@/assets/imgs/grey_bg.jpeg');
  background-size: 1000px;
  position: fixed;
}

.login {
  width: 400px;
  height: 300px;
  background-color: #fff;
  border-radius: 3px;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  opacity: 0.95;
}

.my-form {
  margin-top: 75px;
  width: 300px;
  position: absolute;
  left: 50%;
  top: 36%;
  transform: translate(-50%, -50%);
}

.btns {
  text-align: right; /* 使按钮居中 */
}

.title {
  margin-top: 30px;
  text-align: center;
  color: dodgerblue;
}

.el-form-item {
  margin-left: 5%;
}
</style>