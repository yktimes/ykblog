<template>
  <div>
<div class="container">



  <el-row :gutter="30">
<el-col v-for="(value,key,index) in post_list" v-bind:key="index">


  <el-timeline  >
    <el-timeline-item :timestamp='key' placement="top"
      type="primary"
      size="large">
      <el-card v-for="(v,k) in value" v-bind:key="k">


         <el-button type="success" plain>
              <router-link v-bind:to="{ name: 'PostDetail', params: { id: v[0] }}" >
          {{v[3] }}  发布了 {{v[1]}}
        </router-link>

         </el-button>

          <div >
            <i class="el-icon-timer"></i>
             {{v[4]}}
          </div>

      </el-card>
    </el-timeline-item>

  </el-timeline>
</el-col>




</el-row>

</div>

    <hr>
     <wbc-footer></wbc-footer>


    </div>

</template>

<script>

  import footer from '../../components/Base/footer.vue'

    export default {
        name: "Time",


        data () {
    return {

    hasMore:true,
        next:"",
      messages: '',
          post_list:[],
    }
  },
components: { //定义组件

		'wbc-footer': footer
	},
    methods: {


        InitTime() {
            const path = `/api/time/`
            this.$axios.get(path)
                .then((response) => {

                    this.post_list = response.data.data

                })

        },



    },

     created() { //生命周期函数


           this.InitTime()
        }

    }

</script>


