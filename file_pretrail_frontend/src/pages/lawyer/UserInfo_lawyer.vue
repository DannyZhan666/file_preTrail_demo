<template>
  <div>
    <el-card>
      <div class="info-first-card">
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
          <el-image :src="user.avatarUrl" style="width: 100px; height: 100px" />
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
      <div>
        <el-dialog
            title="修改用户信息"
            v-model:visible="updateDialogVisible.value"
            width="50%"
        >
          <div>
            <el-form :model="updateUser.value" label-width="80px" size="small">

              <el-form-item label="">
                <el-input class="small-input" type="hidden" v-model="updateUser.value.id"></el-input>
              </el-form-item>

              <el-form-item label="姓名">
                <el-input class="small-input" v-model="updateUser.value.username"></el-input>
              </el-form-item>

              <el-form-item label="账号">
                <el-input class="small-input" readonly="readonly" v-model="updateUser.value.userAccount"></el-input>
              </el-form-item>

              <el-form-item label="头像">
                <el-input class="small-input" type="number" v-model="updateUser.value.avatarUrl"></el-input>
              </el-form-item>

              <el-form-item label="手机">
                <el-input class="small-input" type="number" v-model="updateUser.value.phone"></el-input>
              </el-form-item>

              <el-form-item label="邮箱">
                <el-input class="small-input" v-model="updateUser.value.email"></el-input>
              </el-form-item>

              <div class="create-dialog-btn">
                <el-button type="primary" @click="doUpdate">保存</el-button>
                <el-button type="warning" @click="cancel">取消</el-button>
              </div>
            </el-form>
          </div>
        </el-dialog>
      </div>
    </el-card>
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
const updateUser = ref({
  id: "",
  userAccount: '',
  username: '',
  userPassword: '',
  avatarUrl: '',
  phone: '',
  email: '',
  createTime: '',
});

const cancel = () => {
  updateDialogVisible.value = false;
};

const update = () => {
  updateDialogVisible.value = true;
  updateUser.value = {...user.value};
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
/*  await axios.get("/user/current").then(res => {
    let R = res.data;
    user.value = R.data;
    user.value.createTime = dayjs(user.value.createTime).format('YYYY-MM-DD HH:mm:ss');
  });*/
  const res  = await getCurrentUser();
  user.value = res.data.data;
  user.value.createTime = dayjs(user.value.createTime).format('YYYY年MM月DD日 HH:mm:ss');
};

onMounted(() => {
  freshPage();
});

</script>

<style scoped>
.user-info-card {
  margin-top: 60px;
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