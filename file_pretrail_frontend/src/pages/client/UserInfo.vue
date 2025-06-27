<template>
  <div>
    <el-card class="info-first-card" style="width: 75%; margin: 0 auto;">
      <div>
        <h2 class="user-info-title">我的个人信息</h2>
        <el-button class="save" @click="update" type="primary" style="margin-bottom: 20px">修改</el-button>
      </div>
    </el-card>
    <el-card class="box-card user-info-card">
      <el-descriptions title="我的个人信息" border>
        <el-descriptions-item
            :rowspan="2"
            :width="140"
            label="Photo"
            align="center"
        >
          <el-image :src="user.avatarUrl" style="width: 100px; height: 100px"/>
        </el-descriptions-item>
        <el-descriptions-item label="用户名" align="center">
          {{ user.username }}
        </el-descriptions-item>
        <el-descriptions-item label="账号" align="center">
          {{ user.userAccount }}
        </el-descriptions-item>
        <el-descriptions-item label="手机号" align="center">
          {{ user.phone }}
        </el-descriptions-item>
        <el-descriptions-item label="邮箱" align="center">
          {{ user.email }}
        </el-descriptions-item>
        <el-descriptions-item label="注册时间" align="center">
          {{ user.createTime }}
        </el-descriptions-item>
      </el-descriptions>
    </el-card>
    <el-dialog
        title="修改用户信息"
        v-model="updateDialogVisible"
        width="20%"
    >
      <el-form :model="updateUser" label-width="80px" size="small" style="margin: 0 auto; width: 80%;">

        <el-form-item label="姓名">
          <el-input class="small-input" v-model="updateUser.username"></el-input>
        </el-form-item>

        <el-form-item label="头像">
          <!-- 显示当前头像 -->
          <el-image :src="updateUser.avatarUrl" style="width: 100px; height: 100px; margin-bottom: 10px" />

<!--          &lt;!&ndash; 上传新的头像 &ndash;&gt;-->
<!--          <el-upload-->
<!--              action="/file/upload"-->
<!--              :on-success="handleAvatarUpload"-->
<!--              :show-file-list="false"-->
<!--          >-->
<!--            <el-button type="primary">上传新头像</el-button>-->
<!--          </el-upload>-->
        </el-form-item>

        <el-form-item label="手机">
          <el-input class="small-input" type="number" v-model="updateUser.phone"></el-input>
        </el-form-item>

        <el-form-item label="邮箱">
          <el-input class="small-input" v-model="updateUser.email"></el-input>
        </el-form-item>
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
import axios from '@/request';
import {getCurrentUser} from '@/api/user';

const user = ref({
  id: "",
  userAccount: '',
  username: '',
  userPassword: '',
  avatarUrl: '',
  phone: '',
  email: '',
  createTime: '',
});

const updateDialogVisible = ref(false);
const updateUser = ref({ ...user.value });

const cancel = () => {
  updateDialogVisible.value = false;
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
  axios.put("/user/update", updateUser.value).then(res => {
    let ans = res.data;
    if (ans.code === 200) {
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

.user-info-card {
  width: 70%; /* 设置卡片宽度为页面宽度的80% */
  /*margin: 0 auto; 居中置顶显示 */
  margin: 20px 300px; /* 居中显示 */
}

.user-info-title {
  color: cornflowerblue;
  float: left;
  margin-top: -5px;
}

.user-info-data {
  margin-top: 15px;
  margin-left: 45%;
}

br {
  margin-top: 10px;
}

b {
  margin-left: 100px;
}

.el-form-item {
  width: 300px;
}

.save {
  float: right;
  margin-right: 10px;
  margin-top: -10px;
}

.el-form-item {
  margin-left: -5%;
}
</style>
