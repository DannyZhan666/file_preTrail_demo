<template>
  <div>
    <!-- 工单列表 -->
    <el-card class="narrow-card">
      <h2 class="my-title" style="margin-bottom: 20px">已建工单</h2>
      <el-table :data="workOrderList" style="width: 100%">
        <el-table-column type="index" label="序列" width="250" align="center"/>
        <el-table-column prop="jobName" label="工单名" width="auto" align="center"/>
        <el-table-column prop="jobType" label="工单种类" width="auto" align="center"/>
        <el-table-column prop="createTime" label="创建时间" width="auto" align="center"></el-table-column>
        <el-table-column fixed="right" label="Operations" min-width="auto" align="center">
          <template v-slot="scope">
            <el-button link type="primary" size="small" @click="handleClick">
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
    </el-card>
  </div>
</template>

<script setup>
import {ref, onMounted} from 'vue';
import dayjs from 'dayjs';
import {ElMessage} from "element-plus";
import myAxios from "@/request";

const dialogShow = ref(false);
const form = ref({
  jobName: '',
  jobType: '',
  jobIntro: '',
  myFile: [],
  clientBudget: ''
});
const uploadedFiles = ref([]);
const workOrderList = ref([]);
const uploadedNewFiles = ref([]);


const fetchWorkOrders = async (page = 1, pageSize = 10) => {
  try {
    const response = await myAxios.get(`/job/listForClient?page=${page}&pageSize=${pageSize}`);
    if (response.data && response.data.code === 200) {
      workOrderList.value = response.data.data.list.map((job) => ({
        jobId: job.jobId,
        jobName: job.jobName,
        jobType: job.jobType,
        jobIntro: job.jobIntro,
        fid: job.fid,
        // 格式化 createTime 字段
        createTime: dayjs(job.issueDate).format('YYYY-MM-DD HH:mm:ss'),
      }));
    } else {
      console.error('Invalid response data:', response.data);
    }
  } catch (error) {
    console.error('Error fetching work orders:', error);
    this.$message.success('获取工单列表失败');
  }
};


const deleteWorkOrder = async (jobId) => {
  try {
    const response = await axios.delete(`/job/delete/?id=${jobId}`);
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