<template>
  <div id="userRegisterPage" class="whole">
    <div class="register">
    <h2 class="title">用户注册</h2>
    <a-form
      style="max-width: 480px; margin: 0 auto"
      :model="formState"
      name="basic"
      label-align="left"
      :label-col="{ span: 4 }"
      :wrapper-col="{ span: 20 }"
      autocomplete="off"
      @finish="handleSubmit"
    >
      <a-form-item
        label="账号"
        name="user_account"
        :rules="[{ required: true, message: '请输入账号' }]"
      >
        <a-input
          v-model:value="formState.user_account"
          placeholder="请输入账号"
        />
      </a-form-item>
      <a-form-item
        label="密码"
        name="user_password"
        :rules="[
          { required: true, message: '请输入密码' },
          { min: 8, message: '密码不能小于 8 位' },
        ]"
      >
        <a-input-password
          v-model:value="formState.user_password"
          placeholder="请输入密码"
        />
      </a-form-item>
      <a-form-item
        label="确认密码"
        name="check_password"
        :rules="[
          { required: true, message: '请输入确认密码' },
          { min: 8, message: '确认密码不能小于 8 位' },
        ]"
      >
        <a-input-password
          v-model:value="formState.check_password"
          placeholder="请输入确认密码"
        />
      </a-form-item>
      <a-form-item
          label="角色"
          name="user_role"
          :rules="[{ required: true, message: '请选择角色' }]"
      >
        <a-select
            v-model:value="formState.user_role"
            placeholder="请选择角色"
        >
          <a-select-option value="1">一般客户</a-select-option>
          <a-select-option value="2">律师</a-select-option>
        </a-select>
      </a-form-item>
      <a-form-item :wrapper-col="{ offset: 4, span: 20 }">
        <a-button type="primary" html-type="submit" style="width: 100%;">注册</a-button>
      </a-form-item>
    </a-form>
    </div>
  </div>
</template>
<script lang="ts" setup>
import { reactive } from "vue";
import { userRegister } from "@/api/user";
import { message } from "ant-design-vue";
import { useRouter } from "vue-router";

interface FormState {
  user_account: string;
  user_password: string;
  check_password: string;
  user_role: string;
}

const formState = reactive<FormState>({
  user_account: "",
  user_password: "",
  check_password: "",
  user_role: "",
});

const router = useRouter();

/**
 * 提交表单
 * @param values
 */
const handleSubmit = async (values: any) => {
  // 判断两次输入的密码是否一致
  if (formState.user_password !== formState.check_password) {
    message.error("二次输入的密码不一致");
    return;
  }
  const res = await userRegister(values);
  // 注册成功，跳转到登录页面
  if (res.data.code === 200 && res.data.data) {
    message.success("注册成功");
    router.push({
      path: "/homePage",
      replace: true,
    });
  } else {
    message.error("注册失败" + res.data.description);
  }
};
</script>

<style scoped>
.whole {
  width: 100%;
  height: 100%;
  background-image: url('@/assets/imgs/grey_bg.jpeg'); /* 添加背景图片 */
  background-size: cover;
  position: fixed;
}

.register {
  width: 550px;
  background-color: #fff;
  border-radius: 3px;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%); /* 表单居中 */
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  opacity: 0.95;
}

#userRegisterPage .title {
  text-align: center;
  margin-bottom: 16px;
}
</style>
