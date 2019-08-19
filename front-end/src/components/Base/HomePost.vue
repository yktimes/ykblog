<template>
  <div v-bind:class="leftBrdColor" class="media g-brd-around g-brd-gray-light-v4 g-brd-left-1 g-pa-20 g-mb-20">
   <el-row  class="sharelistBox ">

             <el-col :span="24" class="s-item tcommonBox">
            <span class="s-round-date">
                <span class="month" v-html="showInitDate(post.timestamp,'month')+'月'"></span>
                <span class="day" v-html="showInitDate(post.timestamp,'date')"></span>
            </span>
            <header>
                <h1>

             <router-link v-bind:to="{ name: 'PostDetail', params: { id: post.id }}" class="g-text-underline--none--hover">{{ post.title }}</router-link>

                </h1>
<h2>
                 <span>  <router-link v-bind:to="{ path: `/user/${post.author.id}/` }" v-bind:title="post.author.name || post.author.username">
      <img class="g-width-40 g-height-40 rounded-circle rounded" v-bind:src="post.author.avatar" v-bind:alt="post.author.name || post.author.username">

    </router-link></span> <router-link v-bind:to="{ path: `/user/${post.author.id}/` }"><span v-if="post.author.name">{{ post.author.name }}</span><span v-else>{{ post.author.username }}</span></router-link>

                      发表于
          <span>{{ $moment(post.timestamp).fromNow() }}</span>
  <hr>
                     <i class="icon-eye g-pos-rel g-top-1 g-mr-3"></i> {{ post.views }} 次围观 •

                    <span class="rateBox">
                        <router-link v-bind:to="{ path: `/post/${post.id}#like-post` }" class="g-color-gray-dark-v5 g-text-underline--none--hover">
              <i class="icon-heart g-pos-rel g-top-1 g-mr-3"></i> {{ post.likers_count }} 次喜欢 •
            </router-link>
                        <router-link v-bind:to="{ path: `/post/${post.id}#comment-list-wrap` }" class="g-color-gray-dark-v5 g-text-underline--none--hover">
              <i class="icon-bubble g-pos-rel g-top-1 g-mr-3"></i> {{ post.comments_count }} 次评论
            </router-link>
                    </span>
                </h2>
                <div class="ui label" v-if="catclass">
<router-link v-bind:to="{ path: `/Share/?classId=${post.category}` }">  {{catclass[post.category-1].name}} </router-link>
<!--                  <a :href="'/Share?classId='+post.category">{{catclass[post.category-1].name}}</a>-->
<!--                    <a :href="'/Share?classId='+post.category">{{catclass[post.category-1].name}}</a>-->
                </div>
            </header>
            <div class="article-content">
                <p style="text-indent:2em;">
                     <vue-markdown
        :source="post.summary"
        class="markdown-body g-mb-15"
        v-highlight>
      </vue-markdown>
                </p>
                <p  style="max-height:300px;overflow:hidden;text-align:center;">
                    <img :src="post.image" alt="" class="maxW">
                </p>
            </div>
            <div class="viewdetail">
              <ul>

            <router-link v-bind:to="{ name: 'PostDetail', params: { id: post.id }}" class="tcolors-bg">阅读全文</router-link>

          <li v-if="post.author.id == sharedState.user_id" class="list-inline-item g-mr-5">
            <!--<button v-on:click="$emit('edit-post')" class="btn btn-xs u-btn-outline-purple" data-toggle="modal" data-target="#updatePostModal">编辑</button>-->

            <button v-on:click="$emit('edit-post')" class="btn btn-xs u-btn-outline-purple" data-toggle="modal" data-target="#editPostModal">编辑</button>
          </li>
          <li v-if="post.author.id == sharedState.user_id" class="list-inline-item">
            <button v-on:click="$emit('delete-post')" class="btn btn-xs u-btn-outline-red">删除</button>
          </li>
                </ul>
            </div>

</el-col>
     </el-row>


  </div>
</template>

<script>
import store from '../../store'
// 导入 vue-markdown 组件解析 markdown 原文为　HTML
import VueMarkdown from 'vue-markdown'
export default {
  props: ['post','catclass'],



  components: {
    VueMarkdown
  },
  data () {
    return {
      sharedState: store.state
    }
  },
    methods:{
      //初始化时间

         initDate :function(oldDate,full) {
    var odate = new Date(oldDate);
    var year =  odate.getFullYear();
    var month = odate.getMonth()<9? '0' + (odate.getMonth()+1) : odate.getMonth()+1;
    var date = odate.getDate()<10? '0'+odate.getDate() : odate.getDate();
    if(full=='all'){
        var t = oldDate.split(" ")[0];

        return t.split('-')[0]+'年'+t.split('-')[1]+'月'+t.split('-')[2]+'日';
    }else if(full=='year'){
        return year
    }else if(full== 'month'){
        return odate.getMonth()+1
    }else if(full == 'date'){
        return date
    }else if(full== 'newDate'){
        return year+'年'+month+'月'+date+'日';
    }
},

showInitDate: function(oldDate,full){
                // console.log(oldDate,full);
                return this.initDate(oldDate,full)
            },
    },
  computed: {
    leftBrdColor: function () {
      const colors = ['primary', 'blue', 'red', 'purple', 'orange', 'yellow', 'aqua', 'cyan', 'teal', 'brown', 'pink', 'black']
      let index = Math.floor((Math.random() * colors.length))
      return 'g-brd-' + colors[index] + '-left'
    },



  }
}
</script>


<style>
/*分享标题*/
.shareTitle{
    margin-bottom: 40px;
    position: relative;
    border-radius: 5px;
    background: #fff;
    padding:15px;
}
.shareclassTwo{
    width:100%;
}
.shareclassTwo li{
    display: inline-block;
}
.shareclassTwo li a{
    display: inline-block;
    padding:3px 7px;
    margin:5px 10px;
    color:#fff;
    border-radius: 4px;
    background: #64609E;
    border: 1px solid #64609E;
    transition: transform 0.2s linear;
    -webkit-transition: transform 0.2s linear;
}
.shareclassTwo li a:hover{
    transform: translate(0,-3px);
    -webkit-transform: translate(0,-3px);
}
.shareclassTwo li a.active{
    background: #fff;
    color:#64609E;

}
/*文章列表*/
    .sharelistBox{
        transition: all 0.5s ease-out;
        font-size: 15px;
    }


    /*.sharelistBox .viewmore a:hover,.s-item .viewdetail a:hover{
        background: #48456C;
    }*/
</style>
