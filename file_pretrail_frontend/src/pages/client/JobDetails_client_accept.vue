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
          <!-- 用于显示 PDF 页面 -->
          <div v-else class="pdf-container">
            <!-- 设置 canvas 父容器的样式，使其居中 -->
            <canvas ref="pdfCanvasRef" :style="{ width: '70%', height: '970px' }"></canvas>
          </div>
          <!-- 分页控件 -->
          <div class="pagination-container">
            <el-pagination
                v-if="totalPages > 1"
                :current-page="currentPage"
                :page-size="1"
                :total="totalPages"
                layout="prev, pager, next"
                @current-change="handlePdfPageChange"
            />
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-collapse v-model="activeNames">
          <el-collapse-item title="合同预审结果" name="1">
            <el-table :data="paginatedData" border style="width: 100%">
              <el-table-column prop="paragraph" label="段落">
                <template #default="scope">
    <span
        class="clickable-text"
        @click="locatePdfPage(scope.row.pageNum)"
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
                @current-change="handleTablePageChange"
                :current-page="tableCurrentPage"
                :page-size="5"
                layout="prev, pager, next"
                :total="tableData.length"
            />
          </el-collapse-item>
          <el-collapse-item title="工单信息" name="2">
            <el-descriptions class="margin-top" :column="1" :size="size" border>
              <el-descriptions-item label="工单名">{{ jobInfo.jobName }}</el-descriptions-item>
              <el-descriptions-item label="工单种类">{{ jobTypeName }}</el-descriptions-item>
              <el-descriptions-item label="工单简介">{{ jobInfo.jobIntro }}</el-descriptions-item>
              <el-descriptions-item label="客户预算">{{ jobInfo.clientBudget }} 元</el-descriptions-item>
              <el-descriptions-item label="发布日期">{{
                  dayjs(jobInfo.issueDate).format('YYYY年MM月DD日 HH:mm:ss')
                }}
              </el-descriptions-item>
              <el-descriptions-item label="我的预期完成时间">{{
                  dayjs(jobInfo.due).format('YYYY年MM月DD日 HH:mm:ss')
                }}
              </el-descriptions-item>
              <el-descriptions-item label="文件名">{{ jobInfo.fileName }}</el-descriptions-item>
            </el-descriptions>
          </el-collapse-item>
          <el-collapse-item title="律师相关信息" name="3">
            <el-descriptions class="margin-top" :column="1" :size="size" border>
              <el-descriptions-item label="律师">{{ jobInfo.lawyerName }}</el-descriptions-item>
              <el-descriptions-item label="律师预算">{{ jobInfo.lawyerBudget }} 元</el-descriptions-item>
              <el-descriptions-item label="律师评论">{{ jobInfo.lawyerComment }}</el-descriptions-item>
              <el-descriptions-item label="更新时间">{{
                  dayjs(jobInfo.updateTime).format('YYYY年MM月DD日 HH:mm:ss')
                }}
              </el-descriptions-item>
              <el-descriptions-item label="律师预期完成时间">{{
                  dayjs(jobInfo.dueLaw).format('YYYY年MM月DD日 HH:mm:ss')
                }}
              </el-descriptions-item>
            </el-descriptions>
          </el-collapse-item>
        </el-collapse>
        <!-- 添加确认和取消按钮 -->
        <div class="button-group">
          <el-button type="primary" @click="submitForm">确认</el-button>
          <el-button @click="changePage('/NewJobListForClient')">取消</el-button>
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
import {ref, onMounted, computed, nextTick, watch} from 'vue';
import axios from 'axios';
import {useRoute, useRouter} from 'vue-router';
import {ElMessage} from 'element-plus';
import PdfViewer from 'pdf-viewer-vue3';
import dayjs from 'dayjs';
import myAxios from "@/request";
import * as pdfjsLib from 'pdfjs-dist';

// 设置 PDF.js 的 Worker
pdfjsLib.GlobalWorkerOptions.workerSrc = require('pdfjs-dist/build/pdf.worker.entry');


const jobInfo = ref({});
const loading = ref(true);
const error = ref(null);
const pdfUrl = ref(null);
const pdfWidth = ref(800); // 默认宽度
const pdfHeader = ref(null);
const size = ref('small');
const activeNames = ref(['1', '2', '3']); // 默认展开第一个
const currentPage = ref(1); // 当前页码
const tableCurrentPage = ref(1);  // 初始化表格当前页为 1
const totalPages = ref(0); // PDF 总页数
const pageSize = 5; // 每页显示的行数
const pdfCanvasRef = ref(null); // 用于渲染 PDF 页面
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

// 计算当前页的数据
const paginatedData = computed(() => {
  const start = (tableCurrentPage.value - 1) * pageSize;
  const end = start + pageSize;
  return tableData.value.slice(start, end);
});

// 切换展开状态
const toggleExpand = (row: any, field: string) => {
  row[field] = !row[field];
};

// 处理 PDF 分页按钮点击
const handlePdfPageChange = (page: number) => {
  currentPage.value = page;
  renderPage(page);
};
// 处理表格分页按钮点击
const handleTablePageChange = (page: number) => {
  tableCurrentPage.value = page; // 更新表格的当前页码
};

const renderPage = async (pageNum: number) => {
  // console.log("+++++++++++")
  if (!pdfUrl.value || !pdfCanvasRef.value) return;
  // console.log("1")
  // 加载 PDF 文档
  const loadingTask = pdfjsLib.getDocument(pdfUrl.value);
  const pdfDoc = await loadingTask.promise;
  // console.log("2")
  // 获取总页数
  totalPages.value = pdfDoc.numPages;
  // console.log("3")
  // 获取指定页码的页面
  const page = await pdfDoc.getPage(pageNum);

  // console.log(`Rendering page ${pageNum}`); // Debug log

  // 获取 canvas 上下文并设置其尺寸
  const canvas = pdfCanvasRef.value as HTMLCanvasElement;
  const context = canvas.getContext('2d');

  const viewport = page.getViewport({scale: 1});
  canvas.height = viewport.height;
  canvas.width = viewport.width;

  // 渲染页面
  await page.render({canvasContext: context, viewport}).promise;
  console.log(`Page ${pageNum} rendered successfully`); // Debug log
};


// 定位到 PDF 对应页面
const locatePdfPage = (pageNum: number) => {
  console.log('locatePdfPage function called with pageNum:', pageNum);
  currentPage.value = pageNum;  // 更新当前 PDF 页码
  renderPage(pageNum); // 渲染对应的页面
};

const fetchJobDetails = async () => {
  try {
    const id = route.params.id;
    if (!id) throw new Error('无效的工单ID');

    const response = await myAxios.get(`/job/detailsForClient?id=${id}`);
    const data = response.data.data;
    console.log(data)

    jobInfo.value = {
      jobId: data.job_id,
      jobName: data.job_name,
      jobType: data.job_type,
      jobIntro: data.job_intro,
      clientName: data.client_name,
      clientBudget: data.client_budget,
      due: data.due,
      issueDate: data.issue_date,
      paragraph: data.paragraph, // 新增字段
      pageNum: data.page_num, // 新增字段
      paragraphClean: data.paragraph_clean, // 新增字段
      modelPredictDetails: data.model_predict_details, // 新增字段
      modelPredictLabels: data.model_predict_labels, // 新增字段
      fileName: data.file_name,
      lawyerName: data.lawyer_name,
      lawyerBudget: data.lawyer_budget,
      lawyerComment: data.lawyer_comment,
      updateTime: data.update_time,
      dueLaw: data.due_law,
    };

    // 处理表格数据
    tableData.value = data.paragraph.map((_, index) => ({
      paragraph: data.paragraph[index],
      paragraphClean: data.paragraph_clean[index],
      modelPredictDetails: data.model_predict_details[index],
      modelPredictLabels: data.model_predict_labels[index],
      pageNum: data.page_num[index],
    }));

    const blob = base64ToBlob(data.file_content);
    pdfUrl.value = URL.createObjectURL(blob);
    console.log('Generated PDF URL:', pdfUrl.value); // 打印生成的 PDF URL

  } catch (err: any) {
    console.error('获取工单详情失败:', err);
    error.value = err.message || '获取工单信息失败';
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  await fetchJobDetails();
  await nextTick(); // 确保 DOM 已渲染
  // console.log("--------------------")
  if (pdfUrl.value) {
    console.log("--------------------")
    renderPage(currentPage.value); // 渲染 PDF 的第一页
  }
  // pdfCanvasRef 在这里已经指向实际的 canvas 元素
  if (pdfCanvasRef.value) {
    console.log("pdfCanvasRef.value", pdfCanvasRef.value); // 打印 canvas DOM 元素
  }
});

// 监听 pdfUrl 的变化并重新加载 PDF 页面
watch(pdfUrl, (newUrl) => {
  if (newUrl) {
    currentPage.value = 1; // 重置为第一页
    renderPage(currentPage.value);
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

.pdf-container {
  display: flex;
  justify-content: center;  /* 水平居中 */
  align-items: center;      /* 垂直居中 */
  height: 100%;             /* 父容器的高度 */
  background-color: #D6D6D6
}

.pagination-container {
  text-align: center;
  margin-top: 20px;
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