<template>
  <div>
    <el-card class="job-title">
      <div class="title-container">
        <h2 class="my-title">已接工单</h2>
      </div>
    </el-card>
    <!-- 工单列表 -->
    <el-card class="narrow-card">
      <el-table :data="workOrderList" style="width: 100%">
        <el-table-column type="index" label="序列" width="100" align="center"/>
        <el-table-column prop="lawyerName" label="接单律师" width="auto" align="center"/>
<!--        <el-table-column prop="lawyerBudget" label="律师预算" width="auto" align="center"/>-->
        <el-table-column prop="lawyerDue" label="律师预期日期" width="auto" align="center"/>
        <el-table-column prop="jobName" label="工单名" width="auto" align="center"/>
        <el-table-column prop="jobTypeName" label="工单种类" width="auto" align="center"/>
        <el-table-column prop="clientBudget" label="我的预算" width="auto" align="center"/>
        <el-table-column prop="clientDue" label="我的预期日期" width="auto" align="center"/>
        <el-table-column prop="issueDate" label="发布时间" width="auto" align="center"/>
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

<script lang="ts" setup>
import {ref, onMounted} from 'vue';
import axios from 'axios';
import dayjs from 'dayjs';
import {useRouter} from "vue-router";
import myAxios from "@/request";

interface Job {
  jobId: number;
  jobName: string;
  jobType: number;
  clientBudget: number;
  due: string;
  lawyerName: string;
  lawyerBudget: number;
  dueLaw: string;
  jobIntro: string;
  issueDate: string;
  updateTime: string;
}

const router = useRouter();

const dialogShow = ref(false);
const form = ref({
  jobName: '',
  jobType: '',
  jobIntro: '',
  myFile: [],
  clientBudget: ''
});
const page = ref(1); // 当前页码，初始为1
const pageSize = ref(10); // 每页条数，初始为10

const jobTypeMapping: { [key: number]: string } = {
  1: '房地产',
  2: '婚姻',
  3: '公司法'
};

const workOrderList = ref([]);

const fetchWorkOrders = async () => {
  try {
    const response = await myAxios.get(`/job/listNewJobForClient?page=${page.value}&pageSize=${pageSize.value}`);
    if (response.data && response.data.code === 200) {
      // console.log(response.data.data);
      workOrderList.value = response.data.data.map((job: any) => ({
        jobId: job.job_id,
        jobName: job.job_name,
        jobTypeName: jobTypeMapping[job.job_type] || '未知类型',
        clientBudget: job.client_budget,
        clientDue: dayjs(job.due).format('YYYY-MM-DD'),
        lawyerName: job.lawyer_name,
        lawyerBudget: job.lawyer_budget,
        lawyerDue: dayjs(job.due_law).format('YYYY-MM-DD'),
        issueDate: dayjs(job.issue_date).format('YYYY-MM-DD HH:mm:ss'),
        updateTime: dayjs(job.update_date).format('YYYY-MM-DD HH:mm:ss'),
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

const handleDetail = (jobId: any) => {
  router.push({
    name: 'JobDetails_client_accept',
    params: {id: jobId}
  });
};

const writeWorkOrder = () => {
  dialogShow.value = true;
};

const submitWorkOrder = async () => {
  const formData = new FormData();
  formData.append('jobName', form.value.jobName);
  formData.append('jobType', form.value.jobType);
  formData.append('jobIntro', form.value.jobIntro);
  formData.append('myFile', form.value.myFile);
  formData.append('clientBudget', form.value.clientBudget);

  try {
    const response = await axios.post(`/job/create`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    if (response.data && response.data.code === 200) {
      dialogShow.value = false;
      form.value = {jobName: '', jobType: '', jobIntro: '', myFile: [], clientBudget: ''};
      await fetchWorkOrders();
    } else {
      console.error('Invalid response data:', response.data);
    }
  } catch (error) {
    console.error('Error submitting work order:', error);
  }
};

const deleteWorkOrder = async (jobId) => {
  try {
    const response = await myAxios.delete(`/job/deleteNewJobForClient/?id=${jobId}`);
    if (response.data && response.data.code === 200) {
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
  font-weight: bold;
}

/* 增加卡片间垂直间距 */
.job-title + .narrow-card {
  margin-top: 30px !important;
}

.narrow-card {
  width: 85% !important; /* 与标题卡片宽度一致 */
  margin: 0 auto; /* 水平居中 */
  background-color: #fff !important; /* 移除黄色背景 */
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05); /* 添加阴影提升层次感 */
  padding: 20px;
  min-height: 600px; /* 保证与标题卡片高度一致 */
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