<template>
<section>
  <div class="container">
    <nav class="navbar navbar-expand-lg navbar-light bg-light" style="margin-bottom: 20px;">
      <router-link to="/" class="navbar-brand">
        <img src="../../assets/logo.png" width="30" height="30" class="d-inline-block align-top" alt="">
          Design by <a href="" class="g-text-underline--none--hover">YK</a>
      </router-link>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto mt-2 mt-lg-0">
          <li class="nav-item active">
            <router-link to="/" class="nav-link">Home <span class="sr-only">(current)</span></router-link>
          </li>
          <li class="nav-item">
            <router-link to="/ping" class="nav-link">Ping</router-link>
          </li>
        </ul>

        <form v-if="sharedState.is_authenticated" class="form-inline navbar-left mr-auto">
          <input class="form-control mr-sm-2" type="search" placeholder="Search">
          <!-- 暂时先禁止提交，后续实现搜索再改回 type="submit" -->
          <button class="btn btn-outline-success my-2 my-sm-0" type="button">Search</button>
        </form>

        <ul v-if="sharedState.is_authenticated" class="nav navbar-nav navbar-right">
          <li class="nav-item g-mr-20">
<!--            todo {{ sharedState.new_messages_count }}-->
            <router-link v-bind:to="{ path: '/notifications/comments' }" class="nav-link"><i class="icon-education-033 u-line-icon-pro g-color-red g-font-size-16 g-pos-rel g-top-2 g-mr-3"></i> 通知 <span id="new_notifications_count" style="visibility: hidden;" class="u-label g-font-size-11 g-bg-aqua g-rounded-20 g-px-10">0</span></router-link>


          </li>
             <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
              <img v-bind:src="sharedState.user_avatar" class="g-brd-around g-brd-gray-light-v3 g-pa-2 rounded-circle rounded mCS_img_loaded"> {{ sharedState.user_name }}
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
      <div class="u-header__section u-header__section--light g-bg-white g-transition-0_3 g-py-10">
          <nav class="js-mega-menu navbar navbar-expand-lg g-px-0 hs-menu-initialized hs-menu-horizontal">
            <div class="container g-px-15">

              <!-- Responsive Toggle Button -->
              <button class="navbar-toggler navbar-toggler-right btn g-line-height-1 g-brd-none g-pa-0 ml-auto" type="button" aria-label="Toggle navigation" aria-expanded="false" aria-controls="navBar" data-toggle="collapse" data-target="#navBar">
                <span class="hamburger hamburger--collapse g-pa-0">
                  <span class="hamburger-box">
                    <span class="hamburger-inner"></span>
                  </span>
                </span>
              </button>
              <!-- End Responsive Toggle Button -->

              <!-- Navigation -->
              <div class="collapse navbar-collapse align-items-center flex-sm-row g-pt-10 g-pt-5--lg" id="navBar">
                <ul class="navbar-nav g-font-weight-600">

                  <!-- 博客首页 -->
                  <li class="nav-item g-mr-20--lg g-mr-20--xl">
                    <a id="nav-link--blogindex" class="nav-link g-color-aqua--hover g-px-0" href="/">
                      首页
                    </a>
                  </li>
                  <!-- End 博客首页 -->

                    <!-- 博客分类，只支持到三级分类 -->


                            <li class="nav-item hs-has-sub-menu g-mx-20--lg g-mx-20--xl" data-animation-in="fadeIn" data-animation-out="fadeOut">
                                <a id="nav-link--linux" class="nav-link g-color-aqua--hover g-py-7 g-px-0" href="/blog/category/linux/" aria-haspopup="true" aria-expanded="false" aria-controls="nav-submenu--linux">Linux</a>

                                <ul class="hs-sub-menu list-unstyled u-shadow-v11 g-brd-top g-brd-primary g-brd-top-2 g-min-width-220 g-mt-18 g-mt-8--lg--scrolling animated fadeOut" id="nav-submenu--linux" aria-labelledby="nav-link--linux" style="display: none;">


                                            <li class="dropdown-item hs-has-sub-menu ">
                                              <a id="nav-link--linux--linux-basic" class="nav-link" href="/blog/category/linux-basic/" aria-haspopup="true" aria-expanded="false" aria-controls="nav-submenu--linux--linux-basic">运维基础</a>

                                              <ul class="hs-sub-menu list-unstyled u-shadow-v11 g-brd-top g-brd-primary g-brd-top-2 g-min-width-220 g-mt-minus-2" id="nav-submenu--linux--linux-basic" aria-labelledby="nav-link--linux--linux-basic" style="display: none;">

                                                  <li class="dropdown-item">
                                                      <a class="nav-link" href="/blog/category/linux-boot-and-startup-process/">Linux 引导过程与故障排除</a>
                                                  </li>

                                              </ul>
                                            </li>



                                            <li class="dropdown-item">
                                                <a class="nav-link" href="/blog/category/network-security/">网络信息安全</a>
                                            </li>



                                            <li class="dropdown-item">
                                                <a class="nav-link" href="/blog/category/common-linux-services/">常用服务</a>
                                            </li>



                                            <li class="dropdown-item">
                                                <a class="nav-link" href="/blog/category/simple-it-automation/">自动化运维</a>
                                            </li>



                                            <li class="dropdown-item">
                                                <a class="nav-link" href="/blog/category/config-network/">网络配置</a>
                                            </li>



                                            <li class="dropdown-item">
                                                <a class="nav-link" href="/blog/category/load-balance/">负载均衡</a>
                                            </li>



                                            <li class="dropdown-item hs-has-sub-menu ">
                                              <a id="nav-link--linux--log-management" class="nav-link" href="/blog/category/log-management/" aria-haspopup="true" aria-expanded="false" aria-controls="nav-submenu--linux--log-management">日志管理系统</a>

                                              <ul class="hs-sub-menu list-unstyled u-shadow-v11 g-brd-top g-brd-primary g-brd-top-2 g-min-width-220 g-mt-minus-2" id="nav-submenu--linux--log-management" aria-labelledby="nav-link--linux--log-management" style="display: none;">

                                                  <li class="dropdown-item">
                                                      <a class="nav-link" href="/blog/category/elk/">ELK stack</a>
                                                  </li>

                                              </ul>
                                            </li>


                                </ul>
                            </li>



                            <li class="nav-item hs-has-sub-menu g-mx-20--lg g-mx-20--xl" data-animation-in="fadeIn" data-animation-out="fadeOut">
                                <a id="nav-link--python" class="nav-link g-color-aqua--hover g-py-7 g-px-0" href="/blog/category/python/" aria-haspopup="true" aria-expanded="false" aria-controls="nav-submenu--python">Python</a>

                                <ul class="hs-sub-menu list-unstyled u-shadow-v11 g-brd-top g-brd-primary g-brd-top-2 g-min-width-220 g-mt-18 g-mt-8--lg--scrolling animated fadeOut" id="nav-submenu--python" aria-labelledby="nav-link--python" style="display: none;">


                                            <li class="dropdown-item">
                                                <a class="nav-link" href="/blog/category/python-basic/">Python 基础入门</a>
                                            </li>



                                            <li class="dropdown-item hs-has-sub-menu ">
                                              <a id="nav-link--python--python-advance" class="nav-link" href="/blog/category/python-advance/" aria-haspopup="true" aria-expanded="false" aria-controls="nav-submenu--python--python-advance">Python 技能进阶</a>

                                              <ul class="hs-sub-menu list-unstyled u-shadow-v11 g-brd-top g-brd-primary g-brd-top-2 g-min-width-220 g-mt-minus-2" id="nav-submenu--python--python-advance" aria-labelledby="nav-link--python--python-advance" style="display: none;">

                                                  <li class="dropdown-item">
                                                      <a class="nav-link" href="/blog/category/data-structures-and-algorithms-in-python3/">数据结构与算法</a>
                                                  </li>

                                                  <li class="dropdown-item">
                                                      <a class="nav-link" href="/blog/category/python3-spider/">Web 爬虫</a>
                                                  </li>

                                              </ul>
                                            </li>



                                            <li class="dropdown-item">
                                                <a class="nav-link" href="/blog/category/flask/">Flask</a>
                                            </li>


                                </ul>
                            </li>



                            <li class="nav-item hs-has-sub-menu g-mx-20--lg g-mx-20--xl" data-animation-in="fadeIn" data-animation-out="fadeOut">
                                <a id="nav-link--go" class="nav-link g-color-aqua--hover g-py-7 g-px-0" href="/blog/category/go/" aria-haspopup="true" aria-expanded="false" aria-controls="nav-submenu--go">Go</a>

                                <ul class="hs-sub-menu list-unstyled u-shadow-v11 g-brd-top g-brd-primary g-brd-top-2 g-min-width-220 g-mt-18 g-mt-8--lg--scrolling animated fadeOut" id="nav-submenu--go" aria-labelledby="nav-link--go" style="display: none;">


                                            <li class="dropdown-item">
                                                <a class="nav-link" href="/blog/category/go-basic/">Go 基础入门</a>
                                            </li>



                                            <li class="dropdown-item">
                                                <a class="nav-link" href="/blog/category/go-microservices/">Go 微服务</a>
                                            </li>


                                </ul>
                            </li>



                            <li class="nav-item hs-has-sub-menu g-mx-20--lg g-mx-20--xl" data-animation-in="fadeIn" data-animation-out="fadeOut">
                                <a id="nav-link--frontend" class="nav-link g-color-aqua--hover g-py-7 g-px-0" href="/blog/category/frontend/" aria-haspopup="true" aria-expanded="false" aria-controls="nav-submenu--frontend">前端</a>

                                <ul class="hs-sub-menu list-unstyled u-shadow-v11 g-brd-top g-brd-primary g-brd-top-2 g-min-width-220 g-mt-18 g-mt-8--lg--scrolling animated fadeOut" id="nav-submenu--frontend" aria-labelledby="nav-link--frontend" style="display: none;">


                                            <li class="dropdown-item">
                                                <a class="nav-link" href="/blog/category/vuejs/">Vue.js</a>
                                            </li>


                                </ul>
                            </li>



                            <li class="nav-item hs-has-sub-menu g-mx-20--lg g-mx-20--xl" data-animation-in="fadeIn" data-animation-out="fadeOut">
                                <a id="nav-link--cloud" class="nav-link g-color-aqua--hover g-py-7 g-px-0" href="/blog/category/cloud/" aria-haspopup="true" aria-expanded="false" aria-controls="nav-submenu--cloud">容器云</a>

                                <ul class="hs-sub-menu list-unstyled u-shadow-v11 g-brd-top g-brd-primary g-brd-top-2 g-min-width-220 g-mt-18 g-mt-8--lg--scrolling animated fadeOut" id="nav-submenu--cloud" aria-labelledby="nav-link--cloud" style="display: none;">


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
            </div>
          </nav>
        </div>

</section>
</template>

<script>
import store from '../../store'
import axios from 'axios'

export default {
  name: 'Navbar',  //this is the name of the component
  data() {
    return {
      sharedState: store.state
    }
  },
  methods: {
    handlerLogout(e) {
      store.logoutAction()
      this.$toasted.show('You have been logged out.', {icon: 'fingerprint'})
      this.$router.push('/login')
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
