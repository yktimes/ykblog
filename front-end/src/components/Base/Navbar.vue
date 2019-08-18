<!-- 头部公用 -->
<template>
	<div class="">
		<div class="headBack">
			<el-row class="container">
				<el-col :span="24">
					<!-- pc端导航 -->
					<div class="headBox">
						<el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect" :router="true">
							<el-menu-item index="/"><i class="fa fa-wa fa-home"></i> 首页</el-menu-item>
							<el-submenu index="/Share">
								<template slot="title"><i class="fa fa-wa fa-archive"></i> 分类</template>
								<el-menu-item v-for="(item,index) in classListObj" :key="'class1'+index" :index="'/Share/?classId='+item.id">{{item.name}}</el-menu-item>
							</el-submenu>

							<el-menu-item index="/Reward"><i class="fa fa-wa fa-cny"></i> 赞赏</el-menu-item>
							<el-menu-item v-if="sharedState.is_authenticated" index="/notifications/comments">

								<router-link v-bind:to="{ path: '/notifications/comments' }" ><i class="el-icon-chat-dot-square"></i>通知 <span id="new_notifications_count" style="visibility: hidden;" class="u-label  g-bg-aqua g-rounded-20 ">0</span></router-link>
							</el-menu-item>

							<el-menu-item index="/Aboutme"><i class="fa fa-wa fa-vcard"></i> 关于</el-menu-item>
							<el-menu-item index="/Time"><i class="fa fa-wa el-icon-time"></i> 时间轴</el-menu-item>

							<div index="" class="pcsearchbox">


								<i class="el-icon-search pcsearchicon"></i>

								<div class="pcsearchinput" :class="input?'hasSearched':''">

									<form v-if="sharedState.is_authenticated" @submit.prevent="onSubmitSearch">

										<el-input placeholder="搜索" id="searchBody"  suffix-icon="search" v-model="searchForm.body" >
										</el-input>

										<button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
									</form>

								</div>

							</div>


							<div class="userInfo">


								<div v-if="sharedState.is_authenticated" class="haslogin">
									<i class="fa fa-fw fa-user-circle userImg"></i>
									<ul class="haslogin-info">
										<li>
											<router-link v-bind:to="{ path: `/user/${sharedState.user_id}` }" class="dropdown-item"><i class="icon-star g-pos-rel g-top-1 g-mr-5"></i>我的主页</router-link>

										</li>
										<li>
											<router-link v-bind:to="{ name: 'PostsResource' }" class="dropdown-item"><i class="icon-share g-pos-rel g-top-1 g-mr-5"></i> 我的资源</router-link>

										</li>
										<li>
											<router-link v-bind:to="{ name: 'SettingProfile' }" class="dropdown-item"><i class="icon-settings g-pos-rel g-top-1 g-mr-5"></i> 设置</router-link>

										</li>
										<li>
											<a v-on:click="handlerLogout" class="dropdown-item" href="#"><i class="icon-logout g-pos-rel g-top-1 g-mr-5"></i> 退出</a>

										</li>
									</ul>
								</div>

								<div v-else class="nologin">
									<router-link to="/login" class="nav-link"><i class="icon-login "></i> 登录</router-link>
								</div>
							</div>
						</el-menu>
					</div>
					<!-- 移动端导航 -->
					<div class="mobileBox">
						<div class="hideMenu">
							<i @click="pMenu=!pMenu" class="el-icon-menu"></i>
							<el-collapse-transition>
								<el-menu :default-active="activeIndex" class="mlistmenu" v-show="!pMenu"  @open="handleOpen" @close="handleClose" :unique-opened="true" :router="true">
									<el-menu-item index="/"><i class="fa fa-wa fa-home"></i> 首页</el-menu-item>
									<el-submenu index="/Share">
										<template slot="title"><i class="fa fa-wa fa-archive"></i> 分类</template>
										<el-menu-item v-for="(item,index) in classListObj" :key="'class1'+index" :index="'/Share?classId='+item.id">{{item.name}}</el-menu-item>
									</el-submenu>


									<el-menu-item index="/Reward"><i class="fa fa-wa fa-cny"></i> 赞赏</el-menu-item>

									<el-menu-item index="/Aboutme"><i class="fa fa-wa fa-vcard"></i> 关于</el-menu-item>
									<el-menu-item index="/Time"><i class="fa fa-wa el-icon-time"></i> 时间轴</el-menu-item>

									<router-link to="/login">

									<el-menu-item v-if="!sharedState.is_authenticated">
										登录
									</el-menu-item>
									</router-link>
									<router-link to="/register">
									<el-menu-item v-if="!sharedState.is_authenticated">

										注册
									</el-menu-item>
									</router-link>

									<el-submenu v-if="sharedState.is_authenticated" index="3">
										<template slot="title"><i class="fa fa-wa fa-user-circle-o"></i> 我的</template>

										<router-link v-bind:to="{ path: `/user/${sharedState.user_id}` }">
										<el-menu-item >
											我的主页
										</el-menu-item>
										</router-link>

										<router-link v-bind:to="{ name: 'PostsResource' } ">
										<el-menu-item >
											我的资源
										</el-menu-item>
										</router-link>

										<router-link v-bind:to="{ name: 'SettingProfile' } ">
										<el-menu-item >
											设置

										</el-menu-item></router-link>

										<a v-on:click="handlerLogout" href="#">
										<el-menu-item >
											退出

										</el-menu-item></a>

									</el-submenu>
								</el-menu>
							</el-collapse-transition>
							<div class="searchBox ">




								<form v-if="sharedState.is_authenticated" @submit.prevent="onSubmitSearch">


									<router-link v-bind:to="{ path: '/notifications/comments' }" ><i style="font-style:normal" class="icon-education-033 u-line-icon-pro  g-font-size-16 g-pos-rel g-top-5 g-mr-3"></i>  <span id="mobile_new_notifications_count" style="visibility: hidden;" class="u-label g-font-size-11 g-bg-aqua g-rounded-20 g-px-10">0</span></router-link>

									&nbsp;&nbsp;

									<el-input style="width: 200px "  placeholder="" suffix-icon="search" v-model="searchForm.body" @keyup.enter.native="submit" >

									</el-input>  &nbsp;<i class="el-icon-search pcsearchicon" style="font-style:normal"><button class="btn" style="width: 0;height: 0" type="submit"></button></i>

								</form>

							</div>

						</div>
					</div>
				</el-col>
			</el-row>
		</div>

		<div class="headImgBox" >
			<div class="scene">
				<div><span id="luke"></span></div>
			</div>
			<div class="h-information">
				<a href="/Aboutme">
					<img src="../../../static/img/tou.jpg" alt="">
				</a>
				<h2 class="h-description">
					<a href="/Aboutme">
						{{"别停下,哪怕前进了一点点."}}
					</a>
				</h2>
			</div>
		</div>
	</div>
</template>


<script>

	import store from '../../store'
	import axios from 'axios'


	export default {
		data() { //选项 / 数据
			return {

				sharedState: store.state,
				searchForm: {
					body: ''
				},

				userInfo: '', //用户信息
				haslogin: false, //是否已登录
				classListObj: '', //技术分类
				activeIndex: '/', //当前选择的路由模块
				state: '', //icon点击状态
				pMenu: true, //手机端菜单打开
				// path:'',//当前打开页面的路径
				input: '', //input输入内容
				headBg: 'url(../../../static/img/headbg02.jpg)', //头部背景图
				headTou: '', //头像
				projectList: '' //项目列表
			}
		},

		methods: { //事件处理器

			ArtClassData () {


				const path = '/api/posts/classList/'
				this.$axios.get(path)
						.then((response) => {
							// handle success
							this.classListObj = response.data.data

						})
						.catch((error) => {
							// handle error
							console.log(error.response.data)

							// this.$toasted.error(error.response.data.message, { icon: 'fingerprint' })
						})
			},
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
			},

			handleOpen(key, keyPath) { //分组菜单打开
				// console.log(key, keyPath);
			},
			handleClose(key, keyPath) { //分组菜单关闭
				// console.log(key, keyPath);
			},

			handleSelect(key, keyPath) { //pc菜单选择
				//    console.log(key, keyPath);
			},

			routeChange: function() {
				var that = this;
				that.pMenu = true

			}
		},
		components: { //定义组件

		},
		watch: {
			// 如果路由有变化，会再次执行该方法
			'$route': 'routeChange'
		},
		created() { //生命周期函数

			this.ArtClassData()

			this.routeChange();

		},
		mounted() { //页面元素加载完成


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

									$('#mobile_new_notifications_count').text(parseInt(total_notifications_count))
									$('#mobile_new_notifications_count').css('visibility',parseInt(total_notifications_count)  ? 'visible' : 'hidden');
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

<style>
	/*********头部导航栏********/

	/*头部导航栏盒子*/

	.headBack {
		width: 100%;
		background: rgba(40, 42, 44, 0.6);
		/*margin-bottom:30px;*/
		box-shadow: 0 2px 4px 0 rgba(0, 0, 0, .12), 0 0 6px 0 rgba(0, 0, 0, .04);
		position: fixed;
		left: 0;
		top: 0;
		right: 0;
		z-index: 100;
	}

	.headBox li.is-active {
		/*background: #48456C;*/
		background: rgba(73, 69, 107, 0.7);
	}

	.el-menu--horizontal>.el-submenu.is-active .el-submenu__title {
		border-bottom: none!important;
	}

	.headBox .el-menu {
		background: transparent;
		border-bottom: none!important;
	}

	.headBox .el-menu-demo li.el-menu-item,
	.headBox .el-menu--horizontal .el-submenu .el-submenu__title {
		height: 38px;
		line-height: 38px;
		border-bottom: none!important;

	}

	.headBox .el-submenu li.el-menu-item {
		height: 38px;
		line-height: 38px;
	}

	.headBox li .fa-wa {
		vertical-align: baseline;
	}

	.headBox ul li.el-menu-item,
	.headBox ul li.el-menu-item.is-active,
	.headBox ul li.el-menu-item:hover,
	.headBox .el-submenu div.el-submenu__title,
	.headBox .el-submenu__title i.el-submenu__icon-arrow {
		color: #fff;
	}

	.headBox .el-menu--horizontal .el-submenu>.el-menu {
		top: 38px;
		border: none;
		padding: 0;
	}

	.headBox>ul li.el-menu-item:hover,
	.headBox>ul li.el-submenu:hover .el-submenu__title {
		background: #48456C;
		border-bottom: none;
	}

	.headBox>ul .el-submenu .el-menu,
	.headBox>ul .el-submenu .el-menu .el-menu-item {
		background: #48456C;
	}

	.headBox>ul .el-submenu .el-menu .el-menu-item {
		min-width: 0;
	}

	.headBox>ul .el-submenu .el-menu .el-menu-item:hover {
		background: #64609E;
	}

	/*pc搜索框*/

	.headBox .pcsearchbox {
		padding: 0;
		max-width: 170px;
		/*min-width: 30px;*/
		height: 100%;
		line-height: 38px;
		position: absolute;
		top: 0;
		right: 0;
		cursor: pointer;
	}

	.headBox .pcsearchbox:hover .pcsearchinput {
		opacity: 1;
		/*transform: scaleX(1);*/
		visibility: visible;
	}

	.headBox .pcsearchbox i.pcsearchicon {
		color: #fff;
		padding-left: 10px;
	}

	.headBox .pcsearchbox .pcsearchinput {
		width: 180px;
		padding: 10px 20px 10px 20px;
		background: rgba(40, 42, 44, 0.6);
		border-radius: 0 0 2px 2px;
		position: absolute;
		right: 0;
		top: 38px;
		opacity: 0;
		visibility: hidden;
		/*transform: scaleX(0);*/
		transform-origin: right;
		transition: all 0.3s ease-out;
	}

	.headBox .pcsearchbox .hasSearched {
		opacity: 1;
		/*transform: scaleX(1);*/
		visibility: visible;
	}

	.headBox .pcsearchbox .el-input {
		width: 100%;
	}

	.headBox .el-input__inner {
		height: 30px;
		border: none;
		background: #fff;
		/*border: 1px solid #333;*/
		border-radius: 2px;
		padding-right: 10px;
	}

	.headBox .userInfo {
		height: 100%;
		line-height: 38px;
		position: absolute;
		right: 30px;
		top: 0;
		color: #fff;
	}

	.headBox .userInfo a {
		color: #fff;
		font-size: 13px;
		transition: all 0.2s ease-out;
	}

	.headBox .userInfo a:hover {
		color: #48456C;
	}

	.headBox .nologin {
		text-align: right;
	}

	.headBox .haslogin {
		text-align: right;
		position: relative;
		min-width: 80px;
		cursor: pointer;
	}

	.headBox .haslogin:hover ul {
		visibility: visible;
		opacity: 1;
	}

	.headBox .haslogin ul {
		background: rgba(40, 42, 44, 0.6);
		padding: 5px 10px;
		position: absolute;
		right: 0;
		visibility: hidden;
		opacity: 0;
		transition: all 0.3s ease-out;
	}

	.headBox .haslogin ul li {
		border-bottom: 1px solid #48456C;
	}

	.headBox .haslogin ul li:last-child {
		border-bottom: 1px solid transparent;
	}

	/*******移动端*******/

	.mobileBox {
		position: relative;
		height: 38px;
		line-height: 38px;
		color: #fff;
	}

	.hideMenu {
		position: relative;
		width: 100%;
		height: 100%;
		line-height: 38px;
	}

	.hideMenu ul.mlistmenu {
		width: 100%;
		position: absolute;
		left: 0;
		top: 100%;
		box-sizing: border-box;
		z-index: 999;
		box-shadow: 0 2px 6px 0 rgba(0, 0, 0, .12), 0 0 8px 0 rgba(0, 0, 0, .04);
		background: #48456C;
		color: #fff;
		border-right: none;
	}

	.hideMenu .el-submenu .el-menu {
		background: #64609E;
	}

	.hideMenu .el-menu-item,
	.hideMenu .el-submenu__title {
		color: #fff;
	}

	.hideMenu>i {
		position: absolute;
		left: 10px;
		top: 12px;
		width: 30px;
		height: 30px;
		font-size: 16px;
		color: #fff;
		cursor: pointer;
	}

	.hideMenu .el-menu-item,
	.el-submenu__title {
		height: 40px;
		line-height: 40px;
	}

	.mobileBox .searchBox {
		padding-left: 40px;
		width: 100%;
		box-sizing: border-box;
	}

	.mobileBox .searchBox .el-input__inner {
		display: block;
		border-radius: 2px;
		border: none;
		height: 25px;
	}

	.hideMenu ul.mlistmenu.pshow {
		display: block;
	}

	.hideMenu ul.mlistmenu .el-submenu__icon-arrow,
	.mobileBox li.el-menu-item a {
		color: #fff;
	}

	.hideMenu>ul li.el-menu-item:hover,
	.hideMenu>ul li.el-menu-item.is-active {
		background: #48576a;
	}



	/*头部背景图*/

	.headImgBox {
		height: 650px;
		position: relative;
		width: 100%;
		background-size: cover;
		background-position: center 50%;
		background-repeat: no-repeat;
		margin-bottom: 90px;
    background-image: url("../../../static/img/headbg02.jpg");
	}

	.h-information {
		text-align: center;
		width: 70%;
		margin: auto;
		position: relative;
		top: 480px;
		padding: 40px 0;
		font-size: 16px;
		opacity: 0.98;
		background: rgba(230, 244, 249, 0.8);
		border-radius: 5px;
		z-index: 1;
		animation: b 1s ease-out;
		-webkit-animation: b 1s ease-out;
	}

	@-webkit-keyframes b {
		0% {
			-webkit-transform: translateY(90px);
			transform: translateY(90px);
		}
		80% {
			-webkit-transform: translateY(5px);
			transform: translateY(5px)
		}
		90% {
			-webkit-transform: translateY(-5px);
			transform: translateY(-5px)
		}
		to {
			-webkit-transform: translateY(0);
			transform: translateY(0)
		}
	}

	@keyframes b {
		0% {
			-webkit-transform: translateY(90px);
			transform: translateY(90px);
		}
		80% {
			-webkit-transform: translateY(5px);
			transform: translateY(5px)
		}
		90% {
			-webkit-transform: translateY(-5px);
			transform: translateY(-5px)
		}
		to {
			-webkit-transform: translateY(0);
			transform: translateY(0)
		}
	}

	.h-information img {
		width: 100px;
		height: 100px;
		border-radius: 100%;
		transition: all .4s ease-in-out;
		-webkit-transition: all .4s ease-in-out;
		object-fit: cover;
	}

	.h-information img:hover {
		transform: rotate(360deg);
		-webkit-transform: rotate(360deg);
	}

	.h-information h2 {
		margin-top: 20px;
		font-size: 18px;
		font-weight: 700;
		/*font-family: 'Sigmar One';*/
	}
	.h-information h2  a{
		background: linear-gradient(to right, #DF2050, #48456D);
		-webkit-background-clip: text;
		color: transparent;
	}
	.headImgBox .scene {
		width: 100%;
		/*height:300px;*/
		text-align: center;
		font-size: 100px;
		font-weight: 200;
		color: #fff;
		position: absolute;
		left: 0;
		top: 160px;
		font-family: 'Sigmar One', Arial;
		text-shadow: 0 2px 2px #47456d;

	}

	.headImgBox .scene span {
		transform: matrix(1, 0, 0, 1, 0, 0);
		-webkit-transform: matrix(1, 0, 0, 1, 0, 0);
		text-shadow: 1px 1px 0 #ff3f1a, -1px -1px 0 #00a7e0;
	}

	.saying:after {
		content: "|";
		font-family: Arial, sans-serif;
		font-size: 1em;
		/*line-height: 0;*/
		display: inline-block;
		vertical-align: baseline;
		opacity: 1;
		text-shadow: 1px 1px 0 #ff3f1a, -1px -1px 0 #00a7e0;
		animation: caret 500ms infinite;
	}

	@keyframes caret {
		0%,
		100% {
			opacity: 1;
		}
		50% {
			opacity: 0;
		}
	}
</style>
