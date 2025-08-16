<template>
  <div class="job-content">
    <el-row :gutter="30">
      <el-col :span="13">
        <!-- 修改PDF展示部分 -->
        <el-card>
          <div class="pdf-header" ref="pdfHeader">
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
          <embed v-else :src="pdfUrl" height="670px" :width="pdfWidth + 'px'"/>
          <!--          <img src="https://file-pretrail.oss-cn-hangzhou.aliyuncs.com/%E5%B9%BF%E5%9C%BA.png">-->

        </el-card>
      </el-col>
      <el-col :span="11">
        <el-collapse v-model="activeNames">
          <el-collapse-item title="工单信息" name="1">
            <el-descriptions class="margin-top" :column="1" :size="size" border>
              <el-descriptions-item label="工单名">{{ jobInfo.jobName }}</el-descriptions-item>
              <el-descriptions-item label="工单种类">{{ jobTypeName }}</el-descriptions-item>
              <el-descriptions-item label="工单简介">{{ jobInfo.jobIntro }}</el-descriptions-item>
              <el-descriptions-item label="发布用户名">{{ jobInfo.clientName }}</el-descriptions-item>
              <el-descriptions-item label="客户预算">{{ jobInfo.clientBudget }} 元</el-descriptions-item>
              <el-descriptions-item label="发布日期">{{
                  dayjs(jobInfo.issueDate).format('YYYY年MM月DD日 HH:mm:ss')
                }}
              </el-descriptions-item>
              <el-descriptions-item label="预期完成时间">
                {{ dayjs(jobInfo.expectedTime).format('YYYY年MM月DD日 HH:mm:ss') }}
              </el-descriptions-item>
              <el-descriptions-item label="法律文件名">{{ jobInfo.fileName }}</el-descriptions-item>
            </el-descriptions>
          </el-collapse-item>
          <el-collapse-item title="律师填写" name="2">
            <el-descriptions class="margin-top" :column="1" :size="size" border>
              <el-descriptions-item label="您的预算">
                <el-input v-model="lawyerInfo.lawyerBudget"></el-input>
              </el-descriptions-item>
              <el-descriptions-item label="您的预期时间">
                <el-date-picker
                    v-model="lawyerInfo.lawyerExpectedTime"
                    type="datetime"
                    placeholder="选择您的预期时间"
                    style="width: 100%;"
                />
              </el-descriptions-item>
              <el-descriptions-item label="工单批注">
                <el-input v-model="lawyerInfo.lawyerComment"></el-input>
              </el-descriptions-item>
            </el-descriptions>
          </el-collapse-item>
        </el-collapse>
        <!-- 添加确认和取消按钮 -->
        <div class="button-group">
          <el-button type="primary" @click="submitForm">确认</el-button>
          <el-button @click="changePage('/jobList')">取消</el-button>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import {ref, onMounted, computed, nextTick} from 'vue';
import axios from 'axios';
import {useRoute, useRouter} from 'vue-router';
import {ElMessage} from 'element-plus';
import PdfViewer from 'pdf-viewer-vue3';
import dayjs from 'dayjs';
import myAxios from "@/request";


const jobId = ref(null);
const jobInfo = ref({});
const lawyerInfo = ref({
  lawyerBudget: '',
  lawyerComment: '',
  lawyerExpectedTime: '' // 新增字段
});
const loading = ref(true);
const error = ref(null);
const pdfUrl = ref(null);
const pdfWidth = ref(800); // 默认宽度
const pdfHeader = ref(null);
const size = ref('small');
const activeNames = ref(['1', '2']); // 默认展开所有项

const route = useRoute();
const router = useRouter();

const jobTypeMapping = {
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

    const response = await myAxios.get(`/job/details?id=${id}`);
    const data = response.data.data;

    jobInfo.value = {
      jobId: data.job_id,
      jobName: data.job_name,
      jobType: data.job_type,
      jobIntro: data.job_intro,
      clientName: data.client_name,
      clientBudget: data.client_budget,
      expectedTime: dayjs(data.expected_time).format('YYYY-MM-DD HH:mm:ss'),
      issueDate: dayjs(data.issue_date).format('YYYY-MM-DD HH:mm:ss'),
      fileName: data.file_name,
      filePath: data.path,
    };

    lawyerInfo.value = {
      lawyerBudget: '',
      lawyerComment: ''
    };
    const blob = base64ToBlob(data.file_content);
    pdfUrl.value = URL.createObjectURL(blob);

  } catch (err: any) {
    console.error('获取工单详情失败:', err);
    error.value = err.message || '获取工单信息失败';
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  fetchJobDetails();
  await nextTick(); // 确保 DOM 已渲染
  if (pdfHeader.value) {
    pdfWidth.value = pdfHeader.value.offsetWidth; // 动态获取 pdf-header 的宽度
  }
});

const submitForm = async () => {

  const postData = {
    job_id: route.params.id,
    lawyer_budget: lawyerInfo.value.lawyerBudget || 0,
    lawyer_comment: lawyerInfo.value.lawyerComment || '',
    lawyer_expected_time: lawyerInfo.value.lawyerExpectedTime
        ? dayjs(lawyerInfo.value.lawyerExpectedTime).format('YYYY-MM-DDTHH:mm:ss') // 格式化为 ISO 8601 格式
        : ''
  };

  try {
    const response = await myAxios.post('/job/newJob', postData);
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