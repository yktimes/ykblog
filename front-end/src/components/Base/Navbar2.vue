<template>
  <div class="container">







   <nav class="navbar navbar-expand-lg navbar-light bg-light" style="margin-bottom: 20px;">

        <!-- Navigation -->
              <div class="navbar-collapse align-items-center flex-sm-row g-pt-10 g-pt-5--lg collapse" id="navBar" style="">
                <ul class="navbar-nav g-font-weight-600">

                  <!-- 博客首页 -->
                  <li class="nav-item g-mr-20--lg g-mr-20--xl">
                    <a id="nav-link--blogindex" class="nav-link g-color-aqua--hover g-px-0" href="/">
                      首页
                    </a>
                  </li>
                  <!-- End 博客首页 -->


                <li class="nav-item hs-has-sub-menu g-mx-20--lg g-mx-20--xl" data-animation-in="fadeIn" data-animation-out="fadeOut">
                    <a id="nav-link--cloud" class="nav-link g-color-aqua--hover g-py-7 g-px-0" href="/blog/category/cloud/" aria-haspopup="true" aria-expanded="false" aria-controls="nav-submenu--cloud">容器云</a>

                    <ul class="hs-sub-menu list-unstyled u-shadow-v11 g-brd-top g-brd-primary g-brd-top-2 g-min-width-220 g-mt-18 g-mt-8--lg--scrolling" id="nav-submenu--cloud" aria-labelledby="nav-link--cloud" style="display: none;">


                                <li class="dropdown-item">
                                    <a class="nav-link" href="/blog/category/docker/">Docker</a>
                                </li>



                                <li class="dropdown-item">
                                    <a class="nav-link" href="/blog/category/k8s/">Kubernetes</a>
                                </li>



                                <li class="dropdown-item">
                                    <a class="nav-link" href="/blog/category/ceph/">Ceph</a>
                                </li>


                    </ul>
                </li>



                <li class="nav-item g-mx-20--lg g-mx-20--xl">
                    <a id="nav-link--miscellaneous" class="nav-link g-color-aqua--hover g-py-7 g-px-0" href="/blog/category/miscellaneous/">
                        杂记
                    </a>
                </li>



                <li class="nav-item g-mx-20--lg g-mx-20--xl">
                    <a id="nav-link--blog-type" class="nav-link g-color-aqua--hover g-py-7 g-px-0" href="/blog/category/blog-type/">
                        博客类型
                    </a>
                </li>


                    <!-- End: 博客分类，只支持到三级分类 -->

                  <!-- 关于我 -->
                  <li class="nav-item g-mx-20--lg g-mx-20--xl">
                    <a id="nav-link--aboutme" class="nav-link g-color-aqua--hover g-px-0" href="/blog/about/">
                      About
                    </a>
                  </li>
                  <!-- End 关于我 -->

                </ul>
              </div>
              <!-- End Navigation -->

      <router-link to="/" class="navbar-brand">
        <img src="../../assets/logo.png" width="30" height="30" class="d-inline-block align-top" alt="">
          阿T同学
      </router-link>

        <p class="navbar-nav mr-auto  mt-lg-0"  v-if="sharedState.is_authenticated">

            <router-link v-bind:to="{ path: '/notifications/comments' }" class="nav-link"><i class="icon-education-033 u-line-icon-pro g-color-red g-font-size-16 g-pos-rel g-top-2 g-mr-3"></i> 通知 <span id="new_notifications_count" style="visibility: hidden;" class="u-label g-font-size-11 g-bg-aqua g-rounded-20 g-px-10">0</span></router-link>

          </p>

      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto mt-2 mt-lg-0">
          <li class="nav-item active">
            <router-link to="/" class="nav-link">Home <span class="sr-only">(current)</span></router-link>
          </li>

        </ul>

           <form v-if="sharedState.is_authenticated" class="form-inline navbar-left mr-auto" @submit.prevent="onSubmitSearch">
          <input v-model="searchForm.body" id="searchBody" class="form-control mr-sm-2" type="search" placeholder="Search">
          <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
        </form>



        <ul v-if="sharedState.is_authenticated" class="nav navbar-nav navbar-right">

             <li class="nav-item dropdown">
           <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
              <img v-bind:src="sharedState.user_avatar" class="g-brd-around g-brd-gray-light-v3 g-pa-2 g-width-40 g-height-40  rounded-circle rounded mCS_img_loaded g-mt-3 g-mr-15""> {{ sharedState.user_name }}
            </a>

            <div class="dropdown-menu" aria-labelledby="navbarDropdown">
               <router-link v-bind:to="{ path: `/user/${sharedState.user_id}` }" class="dropdown-item"><i class="icon-star g-pos-rel g-top-1 g-mr-5"></i>我的主页</router-link>
              <router-link v-bind:to="{ name: 'PostsResource' }" class="dropdown-item"><i class="icon-share g-pos-rel g-top-1 g-mr-5"></i> Your resource</router-link>
              <router-link v-bind:to="{ name: 'SettingProfile' }" class="dropdown-item"><i class="icon-settings g-pos-rel g-top-1 g-mr-5"></i> 设置</router-link>
              <div class="dropdown-divider"></div>
               <a v-on:click="handlerLogout" class="dropdown-item" href="#"><i class="icon-logout g-pos-rel g-top-1 g-mr-5"></i> 退出</a>
            </div>
          </li>
        </ul>
        <ul v-else class="nav navbar-nav navbar-right">
          <li class="nav-item">
            <router-link to="/login" class="nav-link"><i class="icon-login g-pos-rel g-top-1 g-mr-5"></i> 登录</router-link>
          </li>
        </ul>
      </div>




    </nav>
</div>
  <div class="headerBar">
    <header :style="{background:'url('+backgroundImage+')'}">
      <div class="header-inner">
        <div class="auther">
          <div>
            <a href="/" class="brand">
              <span class="site-title">善良的乌贼</span>
            </a>
          </div>
        </div>
        <nav>
          <ul class="menu">
            <li class="menu-item">
              <router-link to="/">

                <span>首页</span>
              </router-link>
            </li>
            <li class="menu-item">
              <router-link to="/tags">

                <span>标签</span>
              </router-link>
            </li>
            <li class="menu-item">
              <router-link to="/archives">

                <span>归档</span>
              </router-link>
            </li>
            <li class="menu-item">
              <router-link to="/about">

                <span>关于</span>
              </router-link>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  </div>
</template>






<script>
import store from '../../store'
import axios from 'axios'

export default {
  name: 'Navbar',  //this is the name of the component
  data() {
    return {
         backgroundImage: require('../../assets/header-bg.jpg'),
      sharedState: store.state,
        searchForm: {
        body: ''
      }
    }

  },
  methods: {
    handlerLogout(e) {
      store.logoutAction()
      this.$toasted.show('You have been logged out.', {icon: 'fingerprint'})
      this.$router.push('/login')
    },
       onSubmitSearch() {
      if (!this.searchForm.body) {
        $('#searchBody').attr('placeholder', 'keyword required.');
        $('#searchBody').css('background-color', '#fff0f0');

        // 表单验证没通过时，不继续往下执行，即不会通过 axios 调用后端API
        return false
      } else {
        $('#searchBody').css('background-color', '');
      }

      // 提供了搜索关键词后，只需要路由到搜索结果页即可，在 SearchResult.vue 中再请求后端 API
      let q = this.searchForm.body
      let page = 1
      let per_page = 5
      if (typeof this.$route.query.page != 'undefined') {
        page = this.$route.query.page
      }

      if (typeof this.$route.query.per_page != 'undefined') {
        per_page = this.$route.query.per_page
      }

      // 路由到搜索结果页
      this.$router.replace({
        path: '/search',
        query: {
          q: q,
          page: page,
          per_page: per_page
        }
      })
    }
  },
mounted () {
    // 轮询 /api/users/<int:id>/notifications/ 请求用户的新通知
    $(function() {
      let since = 0
      let total_notifications_count = ""  // 总通知计数
      let unread_recived_comments_count = 0  // 收到的新评论通知计数
      let unread_follows_count = 0  // 新粉丝通知计数
      let unread_comments_likes_count  = 0  // 新的喜欢或赞的通知计数
      let unread_messages_count = 0  // 收到的新私信通知计数
      let unread_posts_likes_count = 0  // 新收藏文章的通知计数

      setInterval(function() {
        if (window.localStorage.getItem('yk-token')) {
          // 如果用户已登录，才开始请求 API

          const user_id = window.localStorage.getItem('user_id')
          const path = `/api/users/${user_id}/notifications/?since=${since}`
          axios.get(path)
            .then((response) => {
              // handle success
                console.log(response.data.data.length)
              for(var i = 0; i < response.data.data.length; i++) {
                switch (response.data.data[i].name) {
                  case 'unread_recived_comments_count':
                    unread_recived_comments_count = parseInt(response.data.data[i].payload_json)
                      console.log("unread_recived_comments_count",unread_recived_comments_count)
                      console.log(111111111)
                    break

                    case 'unread_follows_count':
                    unread_follows_count = parseInt(response.data.data[i].payload_json)
                    break

                  case 'unread_comments_likes_count':
                    unread_comments_likes_count  = parseInt(response.data.data[i].payload_json)
                    break

                     case 'unread_messages_count':
                    unread_messages_count = parseInt(response.data.data[i].payload_json)
                    break

                     case 'unread_posts_likes_count':
                    unread_posts_likes_count = parseInt(response.data.data[i].payload_json)
                    break
                }
                since = response.data.data[i].timestamp
              }

              total_notifications_count =parseInt(unread_messages_count )+parseInt(unread_recived_comments_count)+parseInt(unread_follows_count)+parseInt(unread_comments_likes_count)+parseInt(unread_posts_likes_count)
              // 每一次请求之后，根据 total_notifications_count 的值来显示或隐藏徽标
              $('#new_notifications_count').text(parseInt(total_notifications_count))
              $('#new_notifications_count').css('visibility',parseInt(total_notifications_count)  ? 'visible' : 'hidden');
            })
            .catch((error) => {
              // handle error
              console.error(error)
            })
        }
      }, 2000)
    })
  }



}
</script>

<style lang="less" scoped>
header {
  width: 100%;
  height: 325px;
  .header-inner {
    margin: 0 auto;
    padding: 100px 0 70px;
    width: 700px;
    height: 100%;
    position: relative;
  }
  .auther {
    text-align: center;
    color: #fff;
    font-size: 30px;
  }
  .brand {
    position: relative;
    display: inline-block;
    padding: 0 80px;
    line-height: 36px;
  }
  .site-title {
    position: relative;
    top: -50px;
    opacity: 0;
    display: inline-block;
    vertical-align: top;
    line-height: 56px;
    color: #f5f5f5;
    font-weight: normal;
    animation: down 0.2s linear;
    animation-fill-mode: both;
    &:hover{
      transform: scale(1.2);
      transition: all 1s;
    }
  }
  .menu {
    margin: 20px auto 0;
    background: rgba(255, 255, 255, 0.65);
    width: 450px;
    height: 64px;
    display: flex;
    padding: 10px 50px;
    .menu-item {
      flex: 1;
    }
    a {
      color: #333;
      font-size: 16px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: space-between;
      height: 100%;
      position: relative;
      top: -30px;
      opacity: 0;
      animation: down 0.3s 0.2s linear;
      animation-fill-mode: both;
      svg {
        opacity: 0.8;
      }
      span {
        position: relative;
        opacity: 0.8;
        &::before {
          content: '';
          position: absolute;
          width: 100%;
          height: 1px;
          bottom: -5px;
          left: 0;
          background-color: #333;
          visibility: hidden;
          transform: scaleX(0);
          transition: all .2s ease-in-out;
        }
      }
      &:hover {
        svg {
          opacity: 1;
        }
        span {
          opacity: 1;
          &::before {
            visibility: visible;
            transform: scaleX(1);
          }
        }
      }
    }
  }
  .menu-small {
    position: absolute;
    top: 10px;
    left: 10px;
    opacity: 0;
  }
}
@media screen and(max-width: 768px) {
  header {
    min-width: 350px;
    height: 260px;
    .header-inner {
      width: auto;
    }
    nav {
      width: 80%;
      margin: 0 auto;
      .menu {
        width: 100%;
      }
    }
  }
}
</style>
