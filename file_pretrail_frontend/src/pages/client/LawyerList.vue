<template>
  <div>
    <!-- 操作面板 -->
    <el-card class="job-title">
      <div class="title-container">
        <h2 class="my-title">律师列表</h2>
      </div>
    </el-card>
    <!-- 律师列表 -->
    <el-card class="main-card">
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

        <el-table-column prop="avatar_url" label="头像">
          <template #default="scope">
            <a-image :src="scope.row.avatar_url" style="width: 100px; height: 100px" />
          </template>
        </el-table-column>

        <el-table-column prop="phone" label="联系方式">
        </el-table-column>

        <el-table-column prop="email" label="邮箱">
        </el-table-column>

        <el-table-column prop="create_time" label="注册时间">
        </el-table-column>

        <el-table-column label="操作" align="center">
          <template v-slot="scope">
            <el-popconfirm title="确定删除吗？" @confirm="deleteLawyer(scope.row.id)">
              <el-button type="danger" slot="reference">删除</el-button>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
      <div class="pagination-buttons">
        <el-button @click="handlePreviousPage" :disabled="page === 1">上一页</el-button>
        <el-button @click="handleNextPage">下一页</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import {ref, onMounted} from 'vue';
import axios from 'axios';
import dayjs from "dayjs";
import myAxios from "@/request";

const searchKey = ref('');
const lawyerList = ref([]);
const page = ref(1); // 当前页码，初始为1
const pageSize = ref(10); // 每页条数，初始为10

const fetchLawyers = async () => {
  try {
    const response = await myAxios.get(`/user/lawyerList?page=${page.value}&pageSize=${pageSize.value}`);
    if (response.data && response.data.code === 200) {
      // console.log(response.data);
      lawyerList.value = response.data.data.data.map((lawyer) => ({
        id: lawyer.id,
        username: lawyer.username,
        gender: lawyer.gender,
        avatar_url: lawyer.avatar_url,
        phone: lawyer.phone,
        email: lawyer.email,
        // 格式化 createTime 字段
        create_time: dayjs(lawyer.create_time).format('YYYY-MM-DD HH:mm:ss'),
      }));
    } else {
      console.error('Invalid response data:', response.data);
    }
  } catch (error) {
    console.error('Error fetching lawyers:', error);
  }
};

const handleNextPage = () => {
  page.value += 1; // 下一页
  fetchWorkOrders();
};

const handlePreviousPage = () => {
  if (page.value > 1) {
    page.value -= 1; // 上一页
    fetchWorkOrders();
  }
};

const deleteLawyer = async (id) => {
  try {
    const response = await myAxios.delete(`/api/lawyers/${id}`);
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

/* 主卡片样式重置 */
.main-card {
  width: 85% !important; /* 与标题卡片宽度一致 */
  margin: 0 auto; /* 水平居中 */
  background-color: #fff !important; /* 移除黄色背景 */
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05); /* 添加阴影提升层次感 */
  padding: 20px;
  min-height: 600px; /* 保证与标题卡片高度一致 */
}

/* 增加卡片间垂直间距 */
.job-title + .main-card {
  margin-top: 30px !important;
}
.pagination-buttons {
  display: flex;
  justify-content: center; /* 居中对齐 */
  margin-top: 20px; /* 往下移一点 */
  gap: 10px; /* 按钮之间的间距 */
}
</style>
