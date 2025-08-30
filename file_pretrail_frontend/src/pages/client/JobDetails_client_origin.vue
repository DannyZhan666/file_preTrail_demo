<template>
  <div class="job-content">
    <el-row :gutter="30">
      <el-col :span="11">
        <!-- 修改PDF展示部分 -->
        <el-card>
          <div class="pdf-header" ref="pdfHeader">
            <h2 class="center-title">工单关联文件</h2>
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
          <embed v-else :src="pdfUrl" height="670px" :width="pdfWidth + 'px'"/>
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
              <el-descriptions-item label="发布日期">{{
                  dayjs(jobInfo.issueDate).format('YYYY年MM月DD日 HH:mm:ss')
                }}
              </el-descriptions-item>
              <el-descriptions-item label="文件名">{{ jobInfo.fileName }}</el-descriptions-item>
            </el-descriptions>
          </el-collapse-item>
          <el-collapse-item title="合同预审结果" name="2">
            <el-table :data="paginatedData" border style="width: 100%">
              <el-table-column prop="paragraph" label="段落">
                <template #default="scope">
          <span
              class="clickable-text"
              @click="locatePdfPage(scope.row.paragraph)"
          >
            {{
              scope.row.paragraph.length > 20 && !scope.row.expanded
                  ? scope.row.paragraph.slice(0, 20) + '...'
                  : scope.row.paragraph
            }}
          </span>
                  <el-button
                      v-if="scope.row.paragraph.length > 20"
                      type="text"
                      @click="toggleExpand(scope.row, 'expanded')"
                  >
                    {{ scope.row.expanded ? '收起' : '展开' }}
                  </el-button>
                </template>
              </el-table-column>
              <el-table-column prop="paragraphClean" label="段落清理后">
                <template #default="scope">
    <span>
      {{
        scope.row.paragraphClean.length > 20 && !scope.row.expandedClean
            ? scope.row.paragraphClean.slice(0, 20) + '...'
            : scope.row.paragraphClean
      }}
    </span>
                  <el-button
                      v-if="scope.row.paragraphClean.length > 20"
                      type="text"
                      @click="toggleExpand(scope.row, 'expandedClean')"
                  >
                    {{ scope.row.expandedClean ? '收起' : '展开' }}
                  </el-button>
                </template>
              </el-table-column>

              <el-table-column prop="modelPredictDetails" label="模型预测详情">
                <template #default="scope">
    <span>
      {{
        scope.row.modelPredictDetails.length > 20 && !scope.row.expandedDetails
            ? scope.row.modelPredictDetails.slice(0, 20) + '...'
            : scope.row.modelPredictDetails
      }}
    </span>
                  <el-button
                      v-if="scope.row.modelPredictDetails.length > 20"
                      type="text"
                      @click="toggleExpand(scope.row, 'expandedDetails')"
                  >
                    {{ scope.row.expandedDetails ? '收起' : '展开' }}
                  </el-button>
                </template>
              </el-table-column>

              <el-table-column prop="modelPredictLabels" label="模型预测标签">
                <template #default="scope">
    <span>
      {{
        scope.row.modelPredictLabels.length > 20 && !scope.row.expandedLabels
            ? scope.row.modelPredictLabels.slice(0, 20) + '...'
            : scope.row.modelPredictLabels
      }}
    </span>
                  <el-button
                      v-if="scope.row.modelPredictLabels.length > 20"
                      type="text"
                      @click="toggleExpand(scope.row, 'expandedLabels')"
                  >
                    {{ scope.row.expandedLabels ? '收起' : '展开' }}
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
            <el-pagination
                @current-change="handlePageChange"
                :current-page="currentPage"
                :page-size="5"
                layout="prev, pager, next"
                :total="tableData.length"
            />
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
import {ref, onMounted, computed, nextTick} from 'vue';
import axios from 'axios';
import {useRoute, useRouter} from 'vue-router';
import {ElMessage} from 'element-plus';
import PdfViewer from 'pdf-viewer-vue3';
import dayjs from 'dayjs';
import myAxios from "@/request";
import * as pdfjsLib from 'pdfjs-dist';
import pdfjsWorker from 'pdfjs-dist/build/pdf.worker.entry';

// 设置 PDF.js 的 Worker
pdfjsLib.GlobalWorkerOptions.workerSrc = pdfjsWorker;


const jobInfo = ref({});
const loading = ref(true);
const error = ref(null);
const pdfUrl = ref(null);
const pdfWidth = ref(800); // 默认宽度
const pdfHeader = ref(null);
const size = ref('small');
const activeNames = ref(['1', '2', '3']); // 默认展开第一个
const tableData = ref([
  // 示例数据
  {
    paragraph: '这是一个很长的段落文字...',
    paragraphClean: '清理后内容',
    modelPredictDetails: '预测详情',
    modelPredictLabels: '预测标签',
    expanded: false
  },
  // 添加更多数据...
]);
const pdfViewerRef = ref(null); // 引用 PDF 查看器实例
const pdfTextContent = ref<string[][]>([]); // 存储每页的文本内容

const route = useRoute();
const router = useRouter();

const currentPage = ref(1); // 当前页码
const pageSize = 5; // 每页显示的行数

// 计算当前页的数据
const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * pageSize;
  const end = start + pageSize;
  return tableData.value.slice(start, end);
});

// 切换展开状态
const toggleExpand = (row: any, field: string) => {
  row[field] = !row[field];
};

// 处理页码变化
const handlePageChange = (page: number) => {
  currentPage.value = page;
};

// 模糊匹配函数
const isFuzzyMatch = (text1: string, text2: string, threshold = 0.2) => {
  const levenshtein = (a: string, b: string): number => {
    const matrix = Array.from({length: a.length + 1}, (_, i) => Array(b.length + 1).fill(0));
    for (let i = 0; i <= a.length; i++) matrix[i][0] = i;
    for (let j = 0; j <= b.length; j++) matrix[0][j] = j;
    for (let i = 1; i <= a.length; i++) {
      for (let j = 1; j <= b.length; j++) {
        matrix[i][j] = Math.min(
            matrix[i - 1][j] + 1,
            matrix[i][j - 1] + 1,
            matrix[i - 1][j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1)
        );
      }
    }
    return matrix[a.length][b.length];
  };

  const distance = levenshtein(text1, text2);
  const similarity = 1 - distance / Math.max(text1.length, text2.length);
  return similarity >= threshold;
};

// 定位到 PDF 对应页面
const locatePdfPage = (text: string) => {
  console.log('locatePdfPage function called');
  // 定义一个清理函数
  const cleanText = (input: string) => {
    return input
        .toLowerCase() // 转为小写
        .replace(/[\r\n]/g, ' ') // 替换换行符为空格
        .replace(/[^\w\s]/g, '') // 移除标点符号
        .replace(/\s+/g, ' ') // 合并多余空格
        .trim(); // 去除首尾空格
  };
  const cleanedText = cleanText(text); // 清理点击的文本内容
  console.log(cleanedText);

  const pageIndex = pdfTextContent.value.findIndex((page, pageIndex) => {
    console.log(`Checking page ${pageIndex + 1}`);
    const isMatch = page.some((line, lineIndex) => {
      console.log(`Page ${pageIndex + 1}, Line ${lineIndex + 1}: ${line}`);
      return line.includes(cleanedText);
    });
    console.log(`Page ${pageIndex + 1} match result: ${isMatch}`);
    return isMatch;
  });

  if (pageIndex !== -1) {
    console.log(`Matched page index: ${pageIndex}`);
    if (pdfViewerRef.value && 'scrollToPage' in pdfViewerRef.value) {
      (pdfViewerRef.value as any).scrollToPage(pageIndex + 1);
    } else {
      console.warn('PDF viewer reference is invalid or scrollToPage method is missing');
    }
  } else {
    console.warn('No matching page found');
    ElMessage.warning('未找到对应的 PDF 页面');
  }
};

// 加载 PDF 并提取每页文本内容
const loadPdfTextContent = async (pdfUrl: string) => {
  // console.log("==================================");
  // console.log('Loading PDF from URL:', pdfUrl);
  try {
    // const pdf = await PdfViewer.getDocument(pdfUrl).promise;
    const loadingTask = pdfjsLib.getDocument(pdfUrl); // 加载 PDF
    const pdf = await loadingTask.promise; // 获取 PDF 对象
    console.log('PDF loaded successfully:', pdf);

    const totalPages = pdf.numPages;
    // console.log('Total pages in PDF:', totalPages);

    const textContent: string[][] = [];
    for (let i = 1; i <= totalPages; i++) {
      const page = await pdf.getPage(i);
      // console.log(`Processing page ${i}`);
      const text = await page.getTextContent();
      // 清理文本内容：去除多余空格和换行符
      const lines = text.items.map((item: any) => item.str.trim()).filter(line => line !== '');
      const cleanedText = lines.join(' ').toLowerCase(); // 合并为一个字符串并转为小写
      console.log(`Page ${i} text content:`, cleanedText);
      textContent.push([cleanedText]);
    }

    pdfTextContent.value = textContent;
    // console.log('Extracted text content:', pdfTextContent.value);
  } catch (error) {
    console.error('Error loading PDF text content:', error);
  }
};

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
      paragraph: data.paragraph, // 新增字段
      paragraphClean: data.paragraph_clean, // 新增字段
      modelPredictDetails: data.model_predict_details, // 新增字段
      modelPredictLabels: data.model_predict_labels, // 新增字段
    };

    // 处理表格数据
    tableData.value = data.paragraph.map((_, index) => ({
      paragraph: data.paragraph[index],
      paragraphClean: data.paragraph_clean[index],
      modelPredictDetails: data.model_predict_details[index],
      modelPredictLabels: data.model_predict_labels[index],
    }));

    const blob = base64ToBlob(data.file_content);
    // console.log('Generated Blob:', blob); // 打印 Blob 对象
    pdfUrl.value = URL.createObjectURL(blob);
    // console.log('Generated PDF URL:', pdfUrl.value); // 打印生成的 PDF URL

  } catch (err: any) {
    console.error('获取工单详情失败:', err);
    error.value = err.message || '获取工单信息失败';
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  await fetchJobDetails(); // 等待工单详情加载完成
  await nextTick(); // 确保 DOM 已渲染

  if (pdfHeader.value) {
    pdfWidth.value = pdfHeader.value.offsetWidth; // 动态获取 pdf-header 的宽度
  }

  if (pdfUrl.value) {
    console.log('Calling loadPdfTextContent with URL:', pdfUrl.value); // 添加日志
    loadPdfTextContent(pdfUrl.value); // 加载 PDF 文本内容
  } else {
    console.warn('pdfUrl.value is null or undefined');
  }
});

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
  position: fixed;
  bottom: 60px; /* 距离底部 20px */
  right: 80px; /* 距离右侧 20px */
  display: flex;
  gap: 10px; /* 按钮之间的间距 */
}

.button-group .el-button {
  margin-left: 10px;
}

.clickable-text {
  color: #409eff;
  cursor: pointer;
  text-decoration: underline;
}
</style>