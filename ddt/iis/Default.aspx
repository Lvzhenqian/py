<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="Default.aspx.cs" Inherits="Tank.Flash._Default" %>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<!-- saved from url=(0014)about:internet -->
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">

<head id="Head1" runat="server">
    <META   HTTP-EQUIV="Pragma"   CONTENT="no-cache">    
    <META   HTTP-EQUIV="Cache-Control"   CONTENT="no-cache">    
    <META   HTTP-EQUIV="Expires"   CONTENT="0">    
    <title><%=SiteTitle%></title>
    <script type="text/javascript" src="scripts/dandantang.js?0"></script>
    <script type="text/javascript" src="scripts/rightClick.js"></script>
    <script type="text/javascript" src="scripts/swfobject.js"></script>
    <script src="scripts/prototype.js" type="text/javascript"></script>
    <script src="scripts/popup/prototype.js" type="text/javascript"></script>
    <script src="scripts/popup/script/popup.js" type="text/javascript"></script>
    <script type="text/javascript" src="http://static.me.zing.vn/v3/js/zm.xcall-1.01.js" ></script>
    <script type="text/javascript" src="http://static.me.zing.vn/zmjs/zmCore-1.30.min.js" ></script>
    <script type="text/javascript" src="http://static.me.zing.vn/feeddialog/js/feed-dialog-1.00.js" ></script>
    <script type="text/javascript" src="scripts/isSafeFlash.js"></script> 


    <script type="text/javascript">
<!--
	var allowLeave = 2;
	var www="";
	var name="弹弹堂";
        var isPay=false;
	
	function trace(){
		alert("充值");
	}
	function setFavorite(path,titlename,allowvalue)
	{ 
             www=path;
             name=titlename;
             allowLeave=allowvalue;
	}
	function toLocation(url,msg){
		alert(msg);
		closeWindow("1",url);
	}
	
	function addToFavorite()
	{
		var ua = navigator.userAgent.toLowerCase();
		if(ua.indexOf("msie 8")>-1){
			external.AddToFavoritesBar(www,name,'');//IE8
		}else{
			try {
				window.external.addFavorite(www, name);
			} catch(e) {
				try {
					window.sidebar.addPanel(name, www, "");//firefox
				} catch(e) {
					alert("Trình duy?n này kh?ng h? tr? tính n?ng này,h?y dùng Ctrl+D ?? thêm");
				}
			}
		}
	}

	function getLocationUrl(){
		var addurl = document.location.href;
		 //thisMovie("7road-ddt-game").sendSwfNowUrl(addurl.toString());
		try{
			thisMovie("7road-ddt-game").sendSwfNowUrl(addurl.toString());
		}catch(e){
			if (window.clipboardData){
				window.clipboardData.setData("Text", addurl.toString());
			}
			else if (window.netscape){
				try {
					netscape.security.PrivilegeManager.enablePrivilege(addurl.toString());
				} catch (e) {
					alert("Trình duy?t t? ch?i,h?y nh?n F6 ?? nh?n link copy"); 
				}
				
			}else{
				alert("Trình duy?n này kh?ng h? tr? tính n?ng này,h?y nh?n F6 ?? nh?n link copy"); 
			}
		}
	}

     //3.1新功能
    //js与as交互
     function thisMovie(movieName) {
         if (navigator.appName.indexOf("Microsoft") != -1) {
             return window[movieName];
         } else {
             return document[movieName];
         }
     }
     
     var flashCall   =false;     
     function closeWindow(flag,loginUrl) { 
     flashCall   =true;
     if(flag=="0"){
	    top.window.opener=null; 
	    top.window.open("","_self"); 
	    top.window.close(); 
         }else if(flag=="1") { 
              //修改登陆Url
	        window.location.href=loginUrl;
         }
    }
    function setFlashCall(){
	flashCall=true;
    }
    
    //set Active and email
     var dailyTask=-1,dailyActivity=-1,dailyEmail=-1;
    function setDailyTask(_dailyTask){
	dailyTask=_dailyTask;
    }
    function setDailyActivity(_dailyActivity){
	dailyActivity=_dailyActivity;
     }
    function setDailyEmail(_dailyEmail){
	dailyEmail=_dailyEmail;
     }
     
	window.onbeforeunload = function(e)
    	{
           askUserLeave(e);
    }
    function killErrors() //杀掉所有的出错信息
    { 
	    return true; 
    }
	function sandaFillHandler ()
	{
		if(ibw_public.existNameSpace('sdoNewPay'))
		{
			ibw_public.openWidget('sdoNewPay');
		}
	}
	
	function setFlashFocus()
	{
		//document.getElementById('7road-ddt-game').focus();
	}
  window.onerror = killErrors; 

   	function pushfeed(myJSONtext){
	var data = eval('(' + myJSONtext + ')');
	      		//alert(myJSONtext);
				zmf.ui(
			        {		        	
						pub_key: data.pub_key,
						sign_key: data.sign_key,
						action_id: data.actId,
						uid_to: data.userIdTo,
						object_id: data.objectId,
						attach_name: data.attachName,
						attach_href: data.attachHref,
						attach_caption: data.attachCaption,
						attach_des: data.attachDescription,
						media_type: data.mediaType,
						media_img: data.mediaImage,
						media_src: data.mediaSource,
						actlink_text: data.actionLinkText,
						actlink_href: data.actionLinkHref,
						tpl_id: data.tplId,
						suggestion: [data.itemTitle1,data.itemTitle2,data.itemTitle3]
						//suggestion: ["suggestion1", "suggestion2", "suggestion3"]

			        })
	      	}  

// -->
    </script>     
</head>
<body scroll="no"  onload= "setFlashFocus();">
    <style>
      html, body	{ height:100%; }
      body
        {
            margin: 0px auto;
            padding: 0px;
            background-image: url(images/bg_all.jpg);
	     background-repeat: no-repeat;
        background-position: center center;
        overflow:auto; text-align:center;
        }
        *,html,body,embed{cursor:url('<%= Hostname %>/images/cursors/default.cur'), default;}
	    a:hover{cursor:url('<%= Hostname %>/images/cursors/link.cur'), pointer;}
	    input{cursor:url('<%= Hostname %>/images/cursors/input.cur'), text;}
    </style>
<div style="display:none;" id="loginOnUlrStore"><%=LoginOnUrl%></div>
    <table width="100%" height="100%" border="0" cellspacing="0" cellpadding="0">
        <tr>
            <td valign="middle">
                    <table border="0" align="center" cellpadding="0" cellspacing="0">
                        <tr>
                            <td align="center">
                               <div id="gameOuterContainer"  style="cursor:pointer;width:1000px;height:600px;overflow:hidden;background-image:url('images/gameBackGround.jpg');" onclick="showGame();">
                               <div id="gameContainer"  style="width:1000px;height:600px;overflow:hidden;" >
                                <object classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000" id="7road-ddt-game" codebase="http://fpdownload.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=8,0,0,0"
                                    name="Main" width="1000" height="600" align="middle" id="Main">
                                    <param name="allowScriptAccess" value="always" />
                                    <param name="movie" value='http://res256.gn.zing.vn/flash/Loading.swf?<%=Content %>&v=<%=Edition %>&rand=<%=Rand %>&config=http://s256.gn.zing.vn/config.xml&sessionId=<%=Request.QueryString["session_id"] ?? ""%>' />                   
                                    <param name="quality" value="medium" />
                                    <param name="menu" value="false">
                                    <param name="bgcolor" value="#000000" />
                                    <param name="FlashVars" value="<%=AutoParam + "&sex=" + sex %>" />
                                    <param name="allowScriptAccess" value="always" />
                                    <param name="wmode" value="direct" />
                                    
                                    <embed flashVars="<%=AutoParam + "&sex=" + sex %>"  src='http://res256.gn.zing.vn/flash/Loading.swf?<%=Content %>&v=<%=Edition %>&rand=<%=Rand %>&config=http://s256.gn.zing.vn/config.xml' width="1000" height="600"
                                        align="middle" quality="medium" name="Main" allowscriptaccess="always" type="application/x-shockwave-flash"
                                        pluginspage="http://www.macromedia.com/go/getflashplayer" wmode="direct"/>
                                </object>
                               </div>
                               </div>
                            </td>
                        </tr>
                    </table>
            </td>
        </tr>
    </table>

</body>
</html>


