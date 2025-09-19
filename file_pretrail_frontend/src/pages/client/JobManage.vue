<template>
  <div>
    <el-card class="job-title">
      <div class="title-container">
        <h2 class="my-title">已建工单</h2>
      </div>
    </el-card>
    <!-- 工单列表 -->
    <el-card class="main-card">
      <el-table :data="workOrderList" style="width: 100%">
        <el-table-column type="index" label="序列" width="250" align="center"/>
        <el-table-column prop="jobName" label="工单名" width="auto" align="center"/>
        <el-table-column prop="jobType" label="工单种类" width="auto" align="center"/>
        <el-table-column prop="createTime" label="创建时间" width="auto" align="center"></el-table-column>
        <el-table-column fixed="right" label="操作" min-width="auto" align="center">
          <template v-slot="scope">
            <el-button link type="primary" size="small" @click="handleDetail(scope.row.jobId)">
              详情
            </el-button>
            <el-popconfirm
                title="确认删除此工单吗？"
                confirm-button-text="确认"
                cancel-button-text="取消"
                @confirm="() => deleteWorkOrder(scope.row.jobId)"
            >
              <template #reference>
                <el-button link type="danger" size="small">删除</el-button>
              </template>
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
import dayjs from 'dayjs';
import {ElMessage} from "element-plus";
import myAxios from "@/request";
import router from "@/router";

const dialogShow = ref(false);
const form = ref({
  jobName: '',
  jobType: '',
  jobIntro: '',
  myFile: [],
  clientBudget: ''
});
const workOrderList = ref([]);
const page = ref(1); // 当前页码，初始为1
const pageSize = ref(10); // 每页条数，初始为10


const fetchWorkOrders = async () => {
  try {
    const response = await myAxios.get(`/job/listForClient?page=${page.value}&pageSize=${pageSize.value}`);
    if (response.data && response.data.code === 200) {
      workOrderList.value = response.data.data.data.map((job) => ({
        jobId: job.jobId,
        jobName: job.jobName,
        jobType: job.jobType,
        jobIntro: job.jobIntro,
        fid: job.fid,
        // 格式化 createTime 字段
        createTime: dayjs(job.issueDate).format('YYYY-MM-DD HH:mm:ss'),
      })).sort((a, b) => {
        // 按照 createTime 降序排序
        return dayjs(a.createTime).isBefore(dayjs(b.createTime)) ? 1 : -1;
      });
    } else {
      console.error('Invalid response data:', response.data);
    }
  } catch (error) {
    console.error('Error fetching work orders:', error);
    this.$message.success('获取工单列表失败');
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

const handleDetail = (jobId) => {
  router.push({
    name: 'JobDetails_client_origin',
    params: {id: jobId}
  });
};


const deleteWorkOrder = async (jobId) => {
  console.log("Deleting job with ID:", jobId);  // 检查 jobId 是否正确
  try {
    const response = await myAxios.delete(`/job/deleteOriginJobForClient/?id=${jobId}`);
    if (response.data && response.data.code === 200) {
      ElMessage.success('删除成功');
      await fetchWorkOrders();
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

.my-title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.el-form-item label {
  flex-shrink: 0;
  width: 100px;
}

.pagination-buttons {
  display: flex;
  justify-content: center; /* 居中对齐 */
  margin-top: 20px; /* 往下移一点 */
  gap: 10px; /* 按钮之间的间距 */
}

@media (max-width: 768px) {
  .el-table-column {
    width: 100px !important;
  }
}
</style>