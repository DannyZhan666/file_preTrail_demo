<template>
  <div class="job-content">
    <el-row :gutter="30">
      <el-col :span="11">
        <!-- 修改PDF展示部分 -->
        <el-card>
          <div class="pdf-header">
            <h2>工单关联文件</h2>
            <!--            <div>-->
            <!--              <el-button type="primary" icon="el-icon-download" @click="downloadFile" :disabled="!pdfUrl">-->
            <!--                下载文件-->
            <!--              </el-button>-->
            <!--            </div>-->
          </div>

          <!-- 如果 pdfUrl 不存在，显示加载提示 -->
          <div v-if="!pdfUrl" class="loading-text">
            <i class="el-icon-loading"></i>
            正在加载PDF文件...
          </div>
          <!-- 如果 pdfUrl 存在，就渲染 PDF -->
          <embed v-else :src="pdfUrl" height="670px" width="800px"/>
          <!--          <img src="https://file-pretrail.oss-cn-hangzhou.aliyuncs.com/%E5%B9%BF%E5%9C%BA.png">-->

        </el-card>
      </el-col>
      <el-col :span="12">
        <el-collapse v-model="activeNames">
          <el-collapse-item title="文件预审信息" name="1">
            <el-descriptions class="margin-top" :column="1" :size="size" border>
              <el-descriptions-item label="工单名">{{ jobInfo.jobName }}</el-descriptions-item>
              <el-descriptions-item label="工单种类">{{ jobTypeName }}</el-descriptions-item>
              <el-descriptions-item label="工单简介">{{ jobInfo.jobIntro }}</el-descriptions-item>
              <el-descriptions-item label="客户预算">{{ jobInfo.clientBudget }} 元</el-descriptions-item>
              <el-descriptions-item label="发布日期">{{dayjs(jobInfo.issueDate).format('YYYY年MM月DD日 HH:mm:ss') }}</el-descriptions-item>
              <el-descriptions-item label="文件名">{{ jobInfo.fileName }}</el-descriptions-item>
            </el-descriptions>
          </el-collapse-item>
          <el-collapse-item title="工单信息" name="2">
            <el-descriptions class="margin-top" :column="1" :size="size" border>
              <el-descriptions-item label="工单名">{{ jobInfo.jobName }}</el-descriptions-item>
              <el-descriptions-item label="工单种类">{{ jobTypeName }}</el-descriptions-item>
              <el-descriptions-item label="工单简介">{{ jobInfo.jobIntro }}</el-descriptions-item>
              <el-descriptions-item label="客户预算">{{ jobInfo.clientBudget }} 元</el-descriptions-item>
              <el-descriptions-item label="发布日期">{{dayjs(jobInfo.issueDate).format('YYYY年MM月DD日 HH:mm:ss') }}</el-descriptions-item>
              <el-descriptions-item label="我的预期完成时间">{{dayjs(jobInfo.due).format('YYYY年MM月DD日 HH:mm:ss') }}</el-descriptions-item>
              <el-descriptions-item label="文件名">{{ jobInfo.fileName }}</el-descriptions-item>
            </el-descriptions>
          </el-collapse-item>
        </el-collapse>
        <!-- 添加确认和取消按钮 -->
        <div class="button-group">
          <el-button type="primary" @click="submitForm">确认</el-button>
          <el-button @click="changePage('/JobManage')">取消</el-button>
        </div>
        <!--        <el-card>-->
        <!--          <el-descriptions class="margin-top" title="工单信息&#45;&#45;律师" :column="2" :size="size" border>-->
        <!--            <el-descriptions-item v-for="(value, key) in jobInfo" :key="key" :label="key"-->
        <!--                                  v-if="key !== 'path' && key !== 'fileContent'">-->
        <!--              {{ value !== null && value !== undefined ? value : '-' }}-->
        <!--            </el-descriptions-item>-->
        <!--          </el-descriptions>-->
        <!--        </el-card>-->
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
import myAxios from "@/request";


const jobInfo = ref({});
const loading = ref(true);
const error = ref(null);
const pdfUrl = ref(null);
const size = ref('small');
const activeNames = ref(['1', '2', '3']); // 默认展开第一个

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

    const response = await myAxios.get(`/job/details?id=${id}`);
    const data = response.data.data;
    console.log(data)

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

    const blob = base64ToBlob(data.file_content);
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
  const postData = {
    job_id: parseInt(Array.isArray(route.params.id) ? route.params.id[0] : route.params.id, 10) // 将工单 ID 转换为整数类型 // 将工单 ID 包装为对象，添加变量名
  };
  try {
    const response = await myAxios.post('/job/acceptJob', postData);
    console.log('提交表单成功:', response.data);
    ElMessage.success('提交成功');
    changePage('/newJobListForClient');
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
.order-content {
  display: flex;
}

.el-row {
  margin-bottom: 20px;
}

.el-col {
  padding: 10px;
}

.my-el-table {
  width: 100%;
  margin-top: 20px;
}

.clearfix::after {
  content: "";
  display: table;
  clear: both;
}

.embed {
  width: 100%;
  height: auto;
}

.pdf-container {
  width: 100%;
  height: 600px; /* 固定高度 */
  overflow-y: scroll; /* 垂直滚动 */
}

.loading-text {
  text-align: center;
  font-size: 16px;
  color: #666;
}

.button-group {
  position: fixed;
  bottom: 60px; /* 距离底部 20px */
  right: 80px; /* 距离右侧 20px */
  display: flex;
  gap: 10px; /* 按钮之间的间距 */
}

.button-group .el-button {
  margin-left: 10px;
}
</style>