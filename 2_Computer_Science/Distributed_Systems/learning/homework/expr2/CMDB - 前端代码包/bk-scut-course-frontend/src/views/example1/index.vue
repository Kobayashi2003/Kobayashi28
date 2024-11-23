<template>
  <div class="example1-wrapper" >

<!--    <iframe-->
<!--        src="https://apps.ce.bktencent.com/bk-vision/embed/?uid=3mu6wqHieVcLFhAygQ3R5i&bk_app_id=&bk_app_list=['bk-scut-course']&name=&show_copyright=True&watermark=True&time_readonly=False&show_time=True&show_refresh=True&start_time=now/d&end_time=now/d&preview=False&hide_toolbox=False&hide_filter=False&panels=&refresh=False"-->
<!--        style="height: 100%;width: 100%;border: 1px solid rgb(220, 222, 229);">-->
<!--    </iframe>-->


    <div class="fr clearfix mb15">
      <bk-form form-type="inline">
        <bk-form-item label="业务">
          <bk-select
              :disabled="false"
              style="width: 250px;"
              ext-cls="select-custom"
              @change="handleBizChange"
              ext-popover-cls="select-popover-custom"
              searchable>
            <bk-option
                v-for="item in biz_list"
                :key="item.bk_biz_id"
                :id="item.bk_biz_id"
                :name="item.bk_biz_id+'-'+item.bk_biz_name"></bk-option>
          </bk-select>
        </bk-form-item>
        <bk-form-item label="集群">
          <bk-select
              v-model="set_id"
              :disabled="false"
              style="width: 250px;"
              ext-cls="select-custom"
              @change="handleSetChange"
              ext-popover-cls="select-popover-custom"
              searchable>
            <bk-option
                v-for="item in set_list"
                :key="item.bk_set_id"
                :id="item.bk_set_id"
                :name="item.bk_set_id+'-'+item.bk_set_name"></bk-option>
          </bk-select>
        </bk-form-item>
        <bk-form-item label="模块">
          <bk-select
              v-model="module_id"
              :disabled="false"
              style="width: 250px;"
              ext-cls="select-custom"
              @change="handleModuleChange"
              ext-popover-cls="select-popover-custom"
              searchable>
            <bk-option
                v-for="item in module_list"
                :key="item.bk_module_id"
                :id="item.bk_module_id"
                :name="item.bk_module_id+'-'+item.bk_module_name"></bk-option>
          </bk-select>
        </bk-form-item>
        <bk-form-item label="操作人">
          <bk-input placeholder="操作人" @change="handleOperatorChange" v-model="operator" />
        </bk-form-item>
        <bk-form-item>
          <bk-button theme="primary" title="查询" @click="searchHosts">查询</bk-button>
        </bk-form-item>
      </bk-form>
    </div>

    <bk-table style="margin-top: 15px;"
              :data="host_list"
              :size="size"
              :pagination="pagination"
              @page-change="handlePageChange">
      <bk-table-column label="主机ID" prop="bk_host_id" />
      <bk-table-column label="主机IP" prop="bk_host_innerip" />
      <bk-table-column label="操作人" prop="operator" />
      <bk-table-column label="备份维护人" prop="bk_bak_operator" />
      <bk-table-column label="操作" width="150">
        <template slot-scope="props">
          <bk-button theme="primary"
                     text :disabled="props.row.status === '创建中'" @click="getHostDetail(props.row.bk_host_id)">查看详情</bk-button>
        </template>
      </bk-table-column>
    </bk-table>


    <bk-sideslider
        class="bk-layout-component-nelgpjna sideslider1e5ab"
        :is-show.sync="isSidesliderShow"
        :title="('主机详情')"
        :show-mask="false"
        :width="600"
        direction="right">
      <template slot="content">
        <div class="step-detail-container">
          <div class="step-detail-item" v-for="item in host_detail" :key="item.bk_property_id">
            <strong>{{ item.bk_property_name + '：' }}</strong>
            <span>{{ item.bk_property_value ? item.bk_property_value : '无' }}</span>
          </div>
        </div>
      </template>
    </bk-sideslider>
  </div>


</template>

<script>
export default {
  components: {
  },
  data() {
    return {
      size: 'small',
      formData: {
        name: '',
        date: '',
      },
      tableData: [],
      biz_list:  [],  // 业务列表
      set_list:  [],  // 集群列表
      module_list: [],  // 模块列表
      host_list:  [], //主机列表
      host_detail:[], //主机详情列表
      biz_id:null,    // 当前选中的业务ID
      set_id:null,    // 当前选中的集群ID
      module_id:null, // 当权选中的模块ID
      operator:null,  // 操作人
      bak_operator:null,  // 备份维护人
      isSidesliderShow: false,  // 控制侧边栏的显示
      pagination: {
        current: 1,
        count: 0,
        limit: 10,
      },
    };
  },
  created() {
    this.init();
  },
  methods: {
    init() {
      // 页面初始化时执行
      this.getBizData();
    },
    async searchHosts(){
      // TODO：可选优化项：进行参数校验，比如，部分参数为空的话，弹窗提示
      let query_data = {
        "bk_biz_id":this.biz_id
      }
      // 添加可选参数
      if (this.set_id) {
        query_data["bk_set_id"] = this.set_id;
      }

      // 添加可选参数
      if (this.module_id) {
        query_data["bk_module_id"] = this.module_id;
      }

      // 添加可选参数
      if (this.operator) {
        query_data["operator"] = this.operator;
      }

      // TODO:添加额外可选参数：主机ID、主机IP

      console.log('主机查询参数:',query_data)

      const host_res = await this.$store.dispatch('example/getHostsData',query_data,{fromCache:true})
      this.host_list = host_res.data.info
      // TODO：参照bk-table组件文档，实现分页操作
    },
    async getHostDetail(bk_host_id){
      console.log('查询主机详情信息,主机ID：',bk_host_id)
      const host_res = await this.$store.dispatch('example/getHostDetail',{"bk_host_id":bk_host_id},{fromCache:true})
      this.host_detail = host_res.data
      this.isSidesliderShow = true;
    },
    async handleBizChange(newValue, oldValue) {
      console.log('切换了业务，业务ID为：',newValue)
      this.biz_id = newValue
      this.set_id = null    // 每次切换业务ID后，需要重置此前的集群ID和模块ID
      this.module_id = null


      const set_res = await this.$store.dispatch('example/getSetData',{"bk_biz_id":newValue},{fromCache:true})
      this.set_list = set_res.data.info
    },
    async handleSetChange(newValue, oldValue) {
      // 点击集群ID后，查询集群下所有模块，并回显至对应组件
      console.log('切换了集群，集群ID为：',newValue)
      this.set_id = newValue
      this.module_id = null   // 切换集群后，需要重置此前的模块ID
      const module_res = await this.$store.dispatch('example/getModuleData',{"bk_biz_id":this.biz_id,"bk_set_id":this.set_id},{fromCache:true})
      this.module_list = module_res.data.info
    },
    async handleModuleChange(newValue, oldValue) {
      // 点击集群ID后，查询集群下所有模块，并回显至对应组件
      console.log('切换了模块，模块ID为：',newValue)
      this.module_id = newValue
    },
    async getBizData() {
      try {
        // 初始化业务列表数据，渲染至select下拉选框
        console.log('当前环境:',process.env.BK_PAAS_ENVIRONMENT)
        const res = await this.$store.dispatch('example/getBizData', {}, { fromCache: true });
        this.biz_list=res.data.info
        // this.tableData = res.data.info;
        // this.pagination.count = res.data.count;
      } catch (e) {
        console.error(e);
      }
    },
    async handleOperatorChange(value,event){
      try{
        console.log('维护人输入框，当前输入值为',value)
        this.operator = value
      }catch (e) {
        console.error(e)
      }
    },
    toggleTableSize() {
      const size = ['small', 'medium', 'large'];
      const index = (size.indexOf(this.size) + 1) % 3;
      this.size = size[index];
    },
    handlePageChange(page) {
      this.pagination.current = page;
    },
    remove(row) {
      const index = this.tableData.indexOf(row);
      if (index !== -1) {
        this.tableData.splice(index, 1);
      }
    },
    reset(row) {
      // eslint-disable-next-line no-param-reassign
      row.status = '创建中';
    },
  },
};
</script>
