<template>
  <div>
    <el-card class="job-title">
      <div class="title-container">
        <h2 class="my-title">我的个人信息</h2>
        <el-button class="save" @click="update" type="primary" style="margin-bottom: 20px">修改</el-button>
      </div>
    </el-card>
    <el-card class="user-info-card">
      <el-descriptions title="我的个人信息" border>
        <el-descriptions-item :rowspan="2" :width="140" label="Photo" align="center"><el-image :src="user.avatarUrl" style="width: 100px; height: 100px"/></el-descriptions-item>
        <el-descriptions-item label="用户名" align="center">{{ user.username }}</el-descriptions-item>
        <el-descriptions-item label="账号" align="center">{{ user.userAccount }}</el-descriptions-item>
        <el-descriptions-item label="手机号" align="center">{{ user.phone }}</el-descriptions-item>
        <el-descriptions-item label="邮箱" align="center">{{ user.email }}</el-descriptions-item>
        <el-descriptions-item label="注册时间" align="center">{{ user.createTime }}</el-descriptions-item>
      </el-descriptions>
    </el-card>
    <el-dialog title="修改用户信息" v-model="updateDialogVisible" width="20%" custom-class="center-dialog">
      <el-form :model="updateUser" label-width="80px" size="small" style="margin: 0 auto; width: 80%;">
        <el-form-item label="姓名"><el-input class="small-input" v-model="updateUser.username"></el-input></el-form-item>
        <el-form-item label="头像">
          <el-upload
              drag
              class="upload-demo"
              :show-file-list="false"
              :multiple="false"
              :before-upload="beforeUpload"
          >
          <el-icon class="el-icon--upload">
            <upload-filled />
          </el-icon>
          <div class="el-upload__text">
            Drop Photo here or <em>click to upload</em>
          </div>
          </el-upload>
          <p v-if="uploadMessage" style="color: green; margin-top: 10px;">{{ uploadMessage }}</p>
          <p v-if="uploadError" style="color: red; margin-top: 10px;">{{ uploadError }}</p>
        </el-form-item>
        <el-form-item label="性别">
          <el-select v-model="updateUser.gender" placeholder="请选择性别">
            <el-option label="男" :value="1"></el-option>
            <el-option label="女" :value="2"></el-option>
            <el-option label="保密" :value="0"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="手机"><el-input class="small-input" type="number" v-model="updateUser.phone"></el-input></el-form-item>
        <el-form-item label="邮箱"><el-input class="small-input" v-model="updateUser.email"></el-input></el-form-item>
      </el-form>
      <div class="create-dialog-btn" style="text-align: center; margin-top: 20px;">
        <el-button type="primary" @click="doUpdate">保存</el-button>
        <el-button type="warning" @click="cancel">取消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import {ref, onMounted} from 'vue';
import dayjs from 'dayjs';
import {ElMessage} from 'element-plus';
import {getCurrentUser} from '@/api/user';
import myAxios from "@/request";
import {useLoginUserStore} from "@/store/useLoginUserStore";

const loginUserStore = useLoginUserStore();

const user = ref({
  id: "",
  userAccount: '',
  username: '',
  userPassword: '',
  avatarUrl: '',
  phone: '',
  email: '',
  createTime: '',
  gender: 0

});

const uploadMessage = ref("");  // 用于显示上传成功消息
const uploadError = ref("");    // 用于显示上传失败消息
const updateDialogVisible = ref(false);
const updateUser = ref({
  username: '',
  avatarUrl: '',
  phone: '',
  email: '',
  gender: user.value.gender || 0,  // 预设默认值为 "保密"
});

const cancel = () => {
  updateDialogVisible.value = false;
};

// 处理上传之前的校验
const beforeUpload = async (file: File) => {

  // 上传头像请求
  const formData = new FormData();
  formData.append('file', file);

  try {
    // 使用封装的 myAxios 发送请求
    const response = await myAxios.put('/user/avatar', formData, {
      headers: { "Content-Type": "multipart/form-data" },  // 设置上传为表单数据
    });

    // 头像上传成功
    if (response.data.code === 200) {
      updateUser.value.avatarUrl = response.data.data.avatarUrl;  // 假设返回的数据包含 avatarUrl
      uploadMessage.value = "头像上传成功";
      uploadError.value = "";
    } else {
      uploadMessage.value = "";
      uploadError.value = "头像上传失败";
    }

  } catch (error) {
    uploadMessage.value = "";
    uploadError.value = "头像上传失败";
    console.error("头像上传失败:", error);
  }

  // 返回 false 以防止自动上传
  return false;
};


const update = () => {
  console.log("update triggered");
  updateDialogVisible.value = true;
  updateUser.value = {...user.value};
  console.log("updateDialogVisible:", updateDialogVisible.value);
  console.log("updateUser:", updateUser.value);
  console.log("Avatar URL:", user.value.avatarUrl)
};


const doUpdate = () => {
  // 只传递需要更新的字段
  const updatePayload = {
    username: updateUser.value.username,
    avatarUrl: updateUser.value.avatarUrl,
    phone: updateUser.value.phone,
    email: updateUser.value.email,
    gender: updateUser.value.gender
  };
  myAxios.put("/user/update", updatePayload).then(res => {
    let ans = res.data;
    if (ans.code === 200) {
      // 更新 loginUserStore 中的用户名
      loginUserStore.loginUser.username = updateUser.value.username;
      freshPage();
      updateDialogVisible.value = false;
      ElMessage.success(ans.msg);
    } else {
      ElMessage.error(ans.msg);
    }
  });
};

const freshPage = async () => {
  const res = await getCurrentUser();
  console.log("getCurrentUser response:", res);
  user.value = res.data.data;
  user.value.createTime = dayjs(user.value.createTime).format('YYYY年MM月DD日 HH:mm:ss');
  console.log("user:", user.value);
};

onMounted(() => {
  console.log("onMounted triggered");
  freshPage();
});

</script>

<style scoped>

.job-title {
  width: 66% !important;
  margin: 0 auto;
  background-color: #fff !important;
  border-radius: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  padding: 1px;
}

.title-container {
  display: flex;
  justify-content: center;
}

/* 标题样式调整 */
.my-title {
  text-align: center;
  color: #1890ff !important;
  margin: 0 auto; /* 水平居中 */
  margin-bottom: 0px !important;
  font-size: 24px;
  font-weight: bold;
}

/* 增加卡片间垂直间距 */
.job-title + .main-card {
  margin-top: 30px !important;
}

.user-info-card {
  width: 85% !important; /* 与标题卡片宽度一致 */
  margin: 0 auto; /* 水平居中 */
  background-color: #fff !important; /* 移除黄色背景 */
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05); /* 添加阴影提升层次感 */
  padding: 20px;
  min-height: 400px; /* 保证与标题卡片高度一致 */
}

/* 增加卡片间垂直间距 */
.job-title + .user-info-card {
  margin-top: 30px !important;
}


br {
  margin-top: 10px;
}

b {
  margin-left: 100px;
}

.save {
  float: right;
  margin-right: 10px;
  margin-top: -10px;
}

</style>
