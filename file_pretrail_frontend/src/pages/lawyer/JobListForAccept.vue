<template>
  <div>
    <!-- 操作面板 -->
    <el-card class="job-title">
      <div class="title-container">
        <h2 class="my-title">已确认工单列表</h2>
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

        <el-table-column prop="jobTypeName" label="工单种类">
        </el-table-column>

        <el-table-column prop="clientName" label="客户账号">
        </el-table-column>

        <el-table-column prop="clientBudget" label="客户预算">
        </el-table-column>

        <el-table-column prop="createTime" label="客户发布时间">
        </el-table-column>

        <el-table-column prop="updateTime" label="客户确认时间">
        </el-table-column>

        <el-table-column fixed="right" label="操作" min-width="auto" align="center">
          <template v-slot="scope">
            <el-button link type="success" size="large" @click="handleDetail(scope.row.jobId)">
              查看详情
            </el-button>
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

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import dayjs from 'dayjs';
import { useRouter } from "vue-router";
import myAxios from "@/request";

interface Job {
  jobId: number;
  jobName: string;
  jobType: number;
  jobIntro: string;
  clientName: string;
  clientBudget: number;
  issueDate: string;
  updateTime: string;
}

const workOrderList = ref([]);
const page = ref(1); // 当前页码，初始为1
const pageSize = ref(10); // 每页条数，初始为10

const router = useRouter();

const jobTypeMapping: { [key: number]: string } = {
  1: '房地产',
  2: '婚姻',
  3: '公司法'
};

const fetchWorkOrders = async () => {
  try {
    const response = await myAxios.get(`/job/listNewJobForLawyer?page=${page.value}&pageSize=${pageSize.value}`);
    if (response.data && response.data.code === 200) {
      workOrderList.value = response.data.data.map((job: any) => ({
        jobId: job.job_id,
        jobName: job.job_name,
        jobTypeName: jobTypeMapping[job.job_type] || '未知类型',
        jobIntro: job.job_intro,
        clientName: job.client_name,
        clientBudget: job.client_budget,
        createTime: dayjs(job.issue_date).format('YYYY-MM-DD HH:mm:ss'),
        updateTime: dayjs(job.update_time).format('YYYY-MM-DD HH:mm:ss'),
      }));
    } else {
      console.error('Invalid response data:', response.data);
    }
  } catch (error) {
    console.error('Error fetching work orders:', error);
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

const handleDetail = (jobId:any) => {
  router.push({
    name:'jobDetailsForAccept',
    params: { id: jobId }
  });
};

const deleteWorkOrder = async (jobId) => {
  try {
    const response = await myAxios.delete(`/job/deleteNewJobForClient/${jobId}`);
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
  font-weight: bold;
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

.pagination-buttons {
  display: flex;
  justify-content: center; /* 居中对齐 */
  margin-top: 20px; /* 往下移一点 */
  gap: 10px; /* 按钮之间的间距 */
}


</style>
