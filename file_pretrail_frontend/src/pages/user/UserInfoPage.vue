<template>
  <div v-if="user">
    <h2>用户信息</h2>
    <a-descriptions title="User Info">
      <a-descriptions-item label="UserName">{{ user.username }}</a-descriptions-item>
      <a-descriptions-item label="User Account">{{ user.userAccount }}</a-descriptions-item>
      <a-descriptions-item label="Avatar Url">
        <img
            v-if="user.avatarUrl"
            :src="user.avatarUrl"
            alt="Avatar"
            style="width: 50px; height: 50px"
        />
      </a-descriptions-item>
      <a-descriptions-item label="Gender">{{ user.gender === 0 ? "Male" : "Female" }}</a-descriptions-item>
      <a-descriptions-item label="Phone">{{ user.phone }}</a-descriptions-item>
      <a-descriptions-item label="Email">{{ user.email }}</a-descriptions-item>
      <a-descriptions-item label="User Role">{{ user.userRole === 1 ? "Admin" : "User" }}</a-descriptions-item>
      <a-descriptions-item label="Create Time">{{ user.createTime }}</a-descriptions-item>
    </a-descriptions>

    <a-button type="primary" @click="showEditModal">修改</a-button>

    <!-- 修改信息的浮空表单 -->
    <a-modal v-model:visible="isModalVisible" title="修改用户信息" @ok="handleUpdate" @cancel="handleCancel">
      <a-form :model="editForm" :label-col="{ span: 6 }" :wrapper-col="{ span: 14 }">
        <a-form-item label="用户名" name="username">
          <a-input v-model:value="editForm.username" />
        </a-form-item>
        <a-form-item label="账号" name="userAccount">
          <a-input v-model:value="editForm.userAccount" />
        </a-form-item>
        <a-form-item label="性别" name="gender">
          <a-select v-model:value="editForm.gender">
            <a-select-option value="0">Male</a-select-option>
            <a-select-option value="1">Female</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="电话" name="phone">
          <a-input v-model:value="editForm.phone" />
        </a-form-item>
        <a-form-item label="邮箱" name="email">
          <a-input v-model:value="editForm.email" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import { getCurrentUser, updateUserInfo } from "@/api/user";

const user = ref(null);
const isModalVisible = ref(false);
const editForm = reactive({
  username: "",
  userAccount: "",
  gender: 0,
  phone: "",
  email: "",
});

onMounted(async () => {
  try {
    const response = await getCurrentUser();
    console.log("getCurrentUser response:", response);
    console.log("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$");
    if (response && response.data && response.data.code === 200) {
      user.value = response.data.data;
      console.log("user:", user.value);
    }
  } catch (error) {
    console.error("Failed to fetch user info:", error);
  }
});

const showEditModal = () => {
  console.log("showEditModal triggered");
  console.log("user:", user.value);
  if (user.value) {
    Object.assign(editForm, user.value);
    isModalVisible.value = true;
    console.log("isModalVisible:", isModalVisible.value);
    console.log("editForm:", editForm);
  } else {
    console.error("No user data found");
  }
};


const handleUpdate = async () => {
  try {
    const response = await updateUserInfo(editForm);
    if (response && response.data && response.data.code === 0) {
      Object.assign(user.value, editForm); // 更新用户信息
      isModalVisible.value = false;
    }
  } catch (error) {
    console.error("Failed to update user info:", error);
  }
};

const handleCancel = () => {
  isModalVisible.value = false;
};
</script>

<style scoped></style>
