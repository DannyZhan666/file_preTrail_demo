<template>
  <div>
    <!-- 工单列表 -->
    <el-card class="narrow-card">
      <h2 class="my-title" style="margin-bottom: 20px">已接工单</h2>
      <el-table :data="workOrderList" style="width: 100%">
        <el-table-column type="index" label="序列" width="100" align="center"/>
        <el-table-column prop="lawyerName" label="接单律师" width="auto" align="center"/>
        <el-table-column prop="lawyerBudget" label="律师预算" width="auto" align="center"/>
        <el-table-column prop="lawyerDue" label="律师预期日期" width="auto" align="center"/>
        <el-table-column prop="jobName" label="工单名" width="auto" align="center"/>
        <el-table-column prop="jobTypeName" label="工单种类" width="auto" align="center"/>
        <el-table-column prop="clientBudget" label="我的预算" width="auto" align="center"/>
        <el-table-column prop="clientDue" label="我的预期日期" width="auto" align="center"/>
        <el-table-column prop="issueDate" label="发布时间" width="auto" align="center"/>
        <el-table-column fixed="right" label="Operations" min-width="auto" align="center">
          <template v-slot="scope">
            <el-button link type="primary" size="small" @click="handleDetail(scope.row.jobId)">
              详情
            </el-button>
            <el-button link type="danger" size="small">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import {ref, onMounted} from 'vue';
import axios from 'axios';
import dayjs from 'dayjs';
import {useRouter} from "vue-router";

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

const jobTypeMapping: { [key: number]: string } = {
  1: '房地产',
  2: '婚姻',
  3: '公司法'
};

const workOrderList = ref([]);

const fetchWorkOrders = async (page = 1, pageSize = 10) => {
  try {
    const response = await axios.get(`/job/listNewJobForClient?page=${page}&pageSize=${pageSize}`);
    if (response.data && response.data.code === 200) {
      // console.log(response.data.data);
      workOrderList.value = response.data.data.list.map((job: Job) => ({
        jobId: job.jobId,
        jobName: job.jobName,
        jobTypeName: jobTypeMapping[job.jobType] || '未知类型',
        clientBudget: job.clientBudget,
        clientDue:  dayjs(job.due).format('YYYY-MM-DD'),
        lawyerName: job.lawyerName,
        lawyerBudget: job.lawyerBudget,
        lawyerDue: dayjs(job.dueLaw).format('YYYY-MM-DD'),
        issueDate: dayjs(job.issueDate).format('YYYY-MM-DD HH:mm:ss'),
        updateTime: dayjs(job.updateTime).format('YYYY-MM-DD HH:mm:ss'),
      }));
    } else {
      console.error('Invalid response data:', response.data);
    }
  } catch (error) {
    console.error('Error fetching work orders:', error);
  }
};

const handleDetail = (jobId: any) => {
  router.push({
    name: 'jobDetails_client',
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

const deleteWorkOrder = async (id) => {
  try {
    const response = await axios.delete(`/job/delete/${id}`);
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

.narrow-card {
  width: 70%; /* 设置卡片宽度为页面宽度的80% */
  /*margin: 0 auto; 居中置顶显示 */
  margin: 100px 300px; /* 居中显示 */
}

.my-title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.buy {
  float: right;
  margin-right: 20px;
  margin-bottom: 10px;
}

.mid-input {
  width: 100%;
}

.create-dialog-btn {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.my-el-table {
  width: 100%;
  margin-top: 20px;
}

.el-form-item {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.el-form-item label {
  flex-shrink: 0;
  width: 100px;
}

@media (max-width: 768px) {
  .el-table-column {
    width: 100px !important;
  }
}
</style>