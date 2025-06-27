<template>
  <div>
    <!-- 操作面板 -->
    <el-card>
      <div>
        <h2 class="my-title">律师列表</h2>
        <el-input v-model="searchKey" style="width: 240px" @keyup.enter.native="refresh(1)"
                  placeholder="姓名 / 执业证号"></el-input>
        <el-button type="primary" icon="el-icon-search" @click="refresh(1)">搜索</el-button>
      </div>
    </el-card>
    <!-- 律师列表 -->
    <el-card>
      <el-table :data="lawyerList" class="my-el-table">
        <el-table-column label="序号" type="index" width="150">
        </el-table-column>

        <el-table-column prop="username" label="姓名">
        </el-table-column>

        <el-table-column prop="gender" label="性别">
          <template #default="scope">
            {{ getGenderLabel(scope.row.gender) }}
          </template>
        </el-table-column>

        <el-table-column prop="avatarUrl" label="头像">
          <template #default="scope">
            <a-image :src="scope.row.avatarUrl" style="width: 100px; height: 100px" />
          </template>
        </el-table-column>

        <el-table-column prop="phone" label="联系方式">
        </el-table-column>

        <el-table-column prop="email" label="邮箱">
        </el-table-column>

        <el-table-column prop="createTime" label="注册时间">
        </el-table-column>

        <el-table-column label="操作" align="center">
          <template slot-scope="scope">
            <el-popconfirm title="确定删除吗？" @confirm="deleteLawyer(scope.row.id)">
              <el-button type="danger" slot="reference">删除</el-button>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import {ref, onMounted} from 'vue';
import axios from 'axios';
import dayjs from "dayjs";

const searchKey = ref('');
const lawyerList = ref([]);

const fetchLawyers = async (page = 1, pageSize = 10) => {
  try {
    const response = await axios.get(`/user/lawyerList?page=${page}&pageSize=${pageSize}`);
    if (response.data && response.data.code === 200) {
      lawyerList.value = response.data.data.list.map((lawyer) => ({
        id: lawyer.id,
        username: lawyer.username,
        gender: lawyer.gender,
        avatarUrl: lawyer.avatarUrl,
        phone: lawyer.phone,
        email: lawyer.email,
        // 格式化 createTime 字段
        createTime: dayjs(lawyer.createTime).format('YYYY-MM-DD HH:mm:ss'),
      }));
    } else {
      console.error('Invalid response data:', response.data);
    }
  } catch (error) {
    console.error('Error fetching lawyers:', error);
  }
};

const deleteLawyer = async (id) => {
  try {
    const response = await axios.delete(`/api/lawyers/${id}`);
    if (response.data && response.data.code === 200) {
      fetchLawyers();
    } else {
      console.error('Invalid response data:', response.data);
    }
  } catch (error) {
    console.error('Error deleting lawyer:', error);
  }
};

const getGenderLabel = (gender) => {
  return gender === 0 ? '男' : '女';
};

onMounted(() => {
  fetchLawyers();
});
</script>

<style scoped>
.search-input {
  width: 300px;
}

.updateForm {
  width: 80%;
}

.btn-release {
  float: right;
  margin-top: 10px;
  margin-right: 50px;
}

.form-releaseTask {
  height: 300px;
}

.input-content-task {
  width: 500px;
}
</style>
