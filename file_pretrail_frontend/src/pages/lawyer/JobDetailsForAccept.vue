<template>
  <div class="job-content">
    <el-row :gutter="30">
      <el-col :span="13">
        <!-- 修改PDF展示部分 -->
        <el-card>
          <div class="pdf-header">
            <h2 class="center-title">工单关联文件</h2>
<!--                        <div>
                          <el-button type="primary" icon="el-icon-download" @click="downloadFile" :disabled="!pdfUrl">
                            下载文件
                          </el-button>
                        </div>-->
          </div>

          <!-- 如果 pdfUrl 不存在，显示加载提示 -->
          <div v-if="!pdfUrl" class="loading-text">
            <i class="el-icon-loading"></i>
            正在加载PDF文件...
          </div>
          <!-- 如果 pdfUrl 存在，就渲染 PDF -->
          <embed v-else :src="pdfUrl" height="700px" width="950px"/>
          <!--          <img src="https://file-pretrail.oss-cn-hangzhou.aliyuncs.com/%E5%B9%BF%E5%9C%BA.png">-->

        </el-card>
      </el-col>
      <el-col :span="11">
        <el-card>
          <el-descriptions class="margin-top" title="工单信息" :column="1" :size="size" border>
            <!--            <el-descriptions-item v-for="(value, key) in jobInfo" :key="key" :label="key"
                                              v-if="key !== 'path' && key !== 'fileContent'">
                          {{ value !== null && value !== undefined ? value : '-' }}
                        </el-descriptions-item>-->
            <el-descriptions-item label="工单名">{{ jobInfo.jobName }}</el-descriptions-item>
            <el-descriptions-item label="工单种类">{{ jobTypeName }}</el-descriptions-item>
            <el-descriptions-item label="工单简介">{{ jobInfo.jobIntro }}</el-descriptions-item>
            <el-descriptions-item label="发布用户账号">{{ jobInfo.clientAccount }}</el-descriptions-item>
            <el-descriptions-item label="客户预算">{{ jobInfo.clientBudget }} 元</el-descriptions-item>
            <el-descriptions-item label="发布日期">{{dayjs(jobInfo.issueDate).format('YYYY年MM月DD日 HH:mm:ss') }}</el-descriptions-item>
          </el-descriptions>
        </el-card>
        <el-card>
          <el-descriptions class="margin-top" title="客户信息" :column="1" :size="size" border>
            <el-descriptions-item label="客户名">{{ jobInfo.clientName }}</el-descriptions-item>
            <el-descriptions-item label="客户手机号">{{ jobInfo.clientPhone }}</el-descriptions-item>
            <el-descriptions-item label="客户邮箱">{{ jobInfo.clientEmail }}</el-descriptions-item>
          </el-descriptions>
          <!-- 添加确认和取消按钮 -->
          <div class="button-group">
            <el-button @click="changePage('/jobListForAccept')">取消</el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import {ref, onMounted, computed} from 'vue';
import axios from 'axios';
import {useRoute, useRouter} from 'vue-router';
import {ElMessage} from 'element-plus';
import PdfViewer from 'pdf-viewer-vue3';
import dayjs from 'dayjs';


const jobId = ref(null);
const jobInfo = ref({});
const lawyerInfo = ref({
  lawyerBudget: '',
  lawyerComment: ''
});
const loading = ref(true);
const error = ref(null);
const pdfUrl = ref(null);
const pageTotal = ref(30);
const size = ref('small');

const route = useRoute();
const router = useRouter();

const jobTypeMapping: { [key: number]: string } = {
  1: '房地产',
  2: '婚姻',
  3: '公司法'
};

const jobTypeName = computed(() => {
  return jobTypeMapping[jobInfo.value.jobType] || '未知类型';
});

const base64ToBlob = (code: any) => {
  code = code.replace(/[\n\r]/g, '')
  const raw = window.atob(code)
  const rawLength = raw.length
  const uInt8Array = new Uint8Array(rawLength)
  for (let i = 0; i < rawLength; ++i) {
    uInt8Array[i] = raw.charCodeAt(i)
  }
  return new Blob([uInt8Array], {type: 'application/pdf'})
}

const fetchJobDetails = async () => {
  try {
    const id = route.params.id;
    if (!id) throw new Error('无效的工单ID');

    const response = await axios.get(`/job/detailsForAccept?id=${id}`);
    jobInfo.value = response.data.data;

    lawyerInfo.value = {
      lawyerBudget: '',
      lawyerComment: ''
    };
    const blob = base64ToBlob(response.data.data.fileContent);
    pdfUrl.value = URL.createObjectURL(blob);

  } catch (err: any) {
    console.error('获取工单详情失败:', err);
    error.value = err.message || '获取工单信息失败';
  } finally {
    loading.value = false;
  }
};

const downloadFile = () => {
  // 实现文件下载逻辑
};

const submitForm = async () => {
  const postData = Object.assign({
    jobId: route.params.id,
    lawyerBudget: 0,
    lawyerComment: '',
    issueDate: '',
  }, jobInfo.value, {
    lawyerBudget: lawyerInfo.value.lawyerBudget || 0,
    lawyerComment: lawyerInfo.value.lawyerComment || ''
  });

  try {
    const response = await axios.post('/job/newJob', postData);
    console.log('提交表单成功:', response.data);
    ElMessage.success('提交成功');
    changePage('/jobList');
  } catch (error) {
    console.error('提交表单失败:', error);
    ElMessage.error('提交失败');
  }
};

const changePage = (path: any) => {
  router.push(path);
};

/*const filteredJobInfo = computed(() => {
  const filtered:any = {};
  for (const key in jobInfo.value) {
    if (key !== 'path' && key !== 'fileContent') {
      filtered[key] = jobInfo.value[key];
    }
  }
  return filtered;
});*/

onMounted(() => {
  fetchJobDetails();
});
</script>

<style scoped>

.center-title {
  text-align: center;
}
.loading-text {
  text-align: center;
  font-size: 16px;
  color: #666;
}

.button-group {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

.button-group .el-button {
  margin-left: 10px;
}
</style>