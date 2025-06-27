<template>
  <div>
    <!-- 操作面板 -->
    <el-card class="job-title">
      <div class="title-container">
        <h2 class="my-title">工单列表</h2>
      </div>
    </el-card>
    <el-card class="main-card">
      <el-table :data="workOrderList" class="my-el-table">
        <el-table-column label="序号" type="index" width="150">
        </el-table-column>

        <el-table-column prop="jobId" label="工单id">
        </el-table-column>

        <el-table-column prop="jobName" label="工单名">
        </el-table-column>

        <el-table-column prop="clientName" label="客户账号">
        </el-table-column>

        <el-table-column prop="jobTypeName" label="工单种类">
        </el-table-column>

        <el-table-column prop="createTime" label="创建时间">
        </el-table-column>

        <el-table-column label="操作" align="center">
          <template v-slot="scope">
            <el-button type="success" @click="handleDetail(scope.row.jobId)">详情</el-button>
            <el-popconfirm title="确定删除吗？" @confirm="deleteWorkOrder(scope.row.jobId)">
              <el-button type="danger" slot="reference">删除</el-button>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import dayjs from 'dayjs';
import { useRouter } from "vue-router";

interface Job {
  jobId: number;
  jobName: string;
  jobType: number;
  jobIntro: string;
  clientName: string;
  clientBudget: number;
  createTime: string;
}

const workOrderList = ref([]);

const router = useRouter();

const jobTypeMapping: { [key: number]: string } = {
  1: '房地产',
  2: '婚姻',
  3: '公司法'
};

const fetchWorkOrders = async (page = 1, pageSize = 10) => {
  try {
    const response = await axios.get(`/job/list?page=${page}&pageSize=${pageSize}`);
    if (response.data && response.data.code === 200) {
      workOrderList.value = response.data.data.list.map((job: Job) => ({
        jobId: job.jobId,
        jobName: job.jobName,
        jobTypeName: jobTypeMapping[job.jobType] || '未知类型',
        jobIntro: job.jobIntro,
        clientName: job.clientName,
        clientBudget: job.clientBudget,
        createTime: dayjs(job.createTime).format('YYYY-MM-DD HH:mm:ss'),
      }));
    } else {
      console.error('Invalid response data:', response.data);
    }
  } catch (error) {
    console.error('Error fetching work orders:', error);
  }
};

const handleDetail = (jobId:any) => {
  router.push({
    name:'jobDetails',
    params: { id: jobId }
  });
};

const deleteWorkOrder = async (id:any) => {
  try {
    const response = await axios.delete(`/job/delete/${id}`);
    if (response.data && response.data.code === 200) {
      fetchWorkOrders();
    } else {
      console.error('Invalid response data:', response.data);
    }
  } catch (error) {
    console.error('Error deleting work order:', error);
  }
};

onMounted(() => {
  fetchWorkOrders();
});
</script>

<style scoped>
/* 标题片卡样式调整 */
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
}

/* 主卡片样式重置 */
.main-card {
  width: 85% !important; /* 与标题卡片宽度一致 */
  margin: 0 auto;       /* 水平居中 */
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

/* 表格核心样式优化 */
.my-el-table {
  width: 100%; /* 自动填充父容器宽度 */
  margin-top: 20px;
  border-collapse: collapse; /* 关闭默认间隔 */
}

/* 调整表格行高和内边距 */
.my-el-table .el-table__row {
  height: 60px !important;
  min-height: 60px !important;
}

.my-el-table .el-table__cell {
  padding: 15px 0 !important;
}

/* 优化列间距 */
.el-table__column .cell {
  word-break: keep-all;
  white-space: nowrap;
  padding-left: 15px !important;
  padding-right: 15px !important;
}

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
