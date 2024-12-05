<template>
  <div class="search-wrapper">
    <bk-table
        style="margin-top: 15px;"
        :data="recordData">
      <bk-table-column type="index" label="序号" align="center" width="60" />
      <bk-table-column label="主机ID" prop="bk_host_id" width="120" />
      <bk-table-column label="文件目录" prop="bk_file_dir" width="180" />
      <bk-table-column label="文件后缀" prop="bk_file_suffix" width="100" />
      <bk-table-column label="备份文件" prop="bk_backup_name" />
      <bk-table-column label="备份时间" prop="bk_file_create_time" width="200" />
      <bk-table-column label="备份人" prop="bk_file_operator" width="150" />
      <bk-table-column label="备份结果" prop="bk_job_link" width="100">
        <template slot-scope="{ row }">
          <a :href="row.bk_job_link" target="_blank">JOB结果</a>
        </template>
      </bk-table-column>
    </bk-table>
  </div>
</template>

<script>

export default {
  components: {
  },
  data() {
    return {
      list: [],
      recordData: [],
    };
  },
  created() {
    this.getBackupRecord();
  },
  methods: {
    async getBackupRecord() {
      const res = await this.$store.dispatch('example/getBackupRecord', {}, { fromCache: true });
      this.recordData = res.data;
      // TODO：参照bk-table组件文档，实现分页操作
    },
  },
}
;
</script>
