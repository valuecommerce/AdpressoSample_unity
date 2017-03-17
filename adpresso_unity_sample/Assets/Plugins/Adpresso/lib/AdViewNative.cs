//
//  AdViewNative
//  Adpresso SDK
//
//  Copyright 2014 Glossom, inc. All rights reserved.
//
//

#define USE_ADVIEW_IOS_NATIVE

using UnityEngine;
using System.Runtime.InteropServices;
using System;

namespace Adpresso.AdSdk
{
    public class AdViewNative
    {
        private static AdViewNative instance;
        
        public static AdViewNative Instance
        {
            get
            {
                if (instance == null)
                {
#if UNITY_EDITOR
                    instance = new AdViewNative();
#elif UNITY_IPHONE && USE_ADVIEW_IOS_NATIVE
                    instance = new AdViewNativeIos();
#elif UNITY_ANDROID
                    instance = new AdViewNativeAndroid();
#endif
                }
                
                return instance;
            }
        }
        
        public enum Position {
            Top,
            Bottom,
        };
  
        public virtual void SetPosition(AdViewNative.Position position)
        {
        }

        public virtual void Show()
        {
        }
        
        public virtual void Hide()
        {
        }
        
        public virtual void FadeIn()
        {
        }
        
        public virtual void FadeOut()
        {
        }
        
        public virtual void SetPublisherId(string id)
        {
        }
        
        public virtual void SetGapPublisherId(string id)
        {
        }
        
        public virtual void Log(string s)
        {
        }
    }
    

#if UNITY_IPHONE && USE_ADVIEW_IOS_NATIVE && !UNITY_EDITOR

    public class AdViewNativeIos : AdViewNative
    {
      [DllImport("__Internal")]
      private static extern void _AdView_Init();
      public AdViewNativeIos()
      {
        _AdView_Init();
      }

      [DllImport("__Internal")]
      private static extern void _AdView_SetPublisherId(string id);
      public override void SetPublisherId(string id)
      {
        _AdView_SetPublisherId(id);
      }

      [DllImport("__Internal")]
      private static extern void _AdView_SetGapPublisherId(string id);
      public override void SetGapPublisherId(string id)
      {
        _AdView_SetGapPublisherId(id);
      }
  
      [DllImport("__Internal")]
      private static extern void _AdView_ShowHide(bool showHide);
  
      public void ShowHide(bool showHide)
      {
        _AdView_ShowHide(showHide);
      }
  
      public override void Show()
      {
        _AdView_ShowHide(true);
      }
  
      public override void Hide()
      {
        _AdView_ShowHide(false);
      }
  
      [DllImport("__Internal")]
      private static extern void _AdView_FadeIn();
      public override void FadeIn()
      {
        _AdView_FadeIn();
      }

      [DllImport("__Internal")]
      private static extern void _AdView_FadeOut();
      public override void FadeOut()
      {
        _AdView_FadeOut();
      }
  
      [DllImport("__Internal")]
      private static extern void _AdView_SetPosition(AdViewNative.Position position);
      public override void SetPosition(AdViewNative.Position position)
      {
        _AdView_SetPosition(position);
      }
  
      [DllImport("__Internal")]
      private static extern void _AdView_Log(string s);
      public override void Log(string s)
      {
        _AdView_Log(s);
      }
    }

#elif UNITY_ANDROID

  public class AdViewNativeAndroid : AdViewNative
  {
    private AndroidJavaClass AdpressoUnityBridgeClass =  new AndroidJavaClass("com.adpresso.android.unity.AdviewUnityBridge");

    public static AndroidJavaObject getCurrentActivity() {
      AndroidJavaClass unityPlayer = new AndroidJavaClass("com.unity3d.player.UnityPlayer");
      AndroidJavaObject unityActivity = unityPlayer.GetStatic<AndroidJavaObject>("currentActivity");
      
      return unityActivity;
    }

    public AdViewNativeAndroid()
    {
      AndroidJavaObject unityActivity = getCurrentActivity();
      AdpressoUnityBridgeClass.CallStatic("createAdpressoView", unityActivity); 
    }
  
    static bool IsEmulator()
    {
      return Application.platform != RuntimePlatform.Android;
    }
  
    private void _SetPublisherId(string method, string id)
    {
      if (IsEmulator())
      {
        return;
      }

      AdpressoUnityBridgeClass.CallStatic(method, id);
    }
  
    public override void SetPublisherId(string id)
    {
      _SetPublisherId("setPublisherID", id);
    }

    public override void SetGapPublisherId(string id)
    {
      _SetPublisherId("setGapPublisherID", id);
    }
  
    // These correspond to the values in android.view.View
    // http://developer.android.com/reference/android/view/View.html
    public enum Visibility : int {
      VISIBLE = 0,
      INVISIBLE = 4,
      GONE = 8
    }
  
    public void SetVisibility(Visibility visibility)
    {
      AdpressoUnityBridgeClass.CallStatic("setViewVisibility", (int)visibility);
    }

    public override void SetPosition(AdViewNative.Position position)
    {
      AdpressoUnityBridgeClass.CallStatic("setPosition", (int)position);
    }
	
    public override void Show()
    {
      AdpressoUnityBridgeClass.CallStatic("load", getCurrentActivity());

      SetVisibility(Visibility.VISIBLE);
    }
  
    public override void Hide()
    {
      SetVisibility(Visibility.INVISIBLE);
    }
  }

#endif

}
