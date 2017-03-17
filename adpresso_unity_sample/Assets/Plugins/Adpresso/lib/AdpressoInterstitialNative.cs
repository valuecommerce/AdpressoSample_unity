//
//  AdpressoInterstitialNative
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
    public class AdpressoInterstitialNative
    {
        private static AdpressoInterstitialNative instance;
        
        public static AdpressoInterstitialNative Instance
        {
            get
            {
                if (instance == null)
                {
          //TODO reaise Error
                }
                
                return instance;
            }
        }
        
        public static void initWithPublisherId(string publisherId , string callbackName )
        {
          #if UNITY_EDITOR
          instance = new AdpressoInterstitialNative();
          #elif UNITY_IPHONE && USE_ADVIEW_IOS_NATIVE
      instance = new AdpressoInterstitialNativeIos(publisherId, callbackName);
          #elif UNITY_ANDROID
      instance = new AdpressoInterstitialNativeAndroid(publisherId, callbackName);
          #endif
        } 
        
        public virtual void Show()
        {
        }
        
        public virtual void Cancel()
        {
        }
        
        public virtual void Log(string s)
        {
        }
    }
    

#if UNITY_IPHONE && USE_ADVIEW_IOS_NATIVE && !UNITY_EDITOR

    public class AdpressoInterstitialNativeIos : AdpressoInterstitialNative
    {
      [DllImport("__Internal")]
    private static extern void _AdpressoIntersitial_Init(string publisherId, string callbackName);
      public AdpressoInterstitialNativeIos(string publisherId, string callbackName)
      {
      _AdpressoIntersitial_Init(publisherId, callbackName);
      }
  
      [DllImport("__Internal")]
      private static extern void _AdpressoIntersitial_Show();
      public override void Show()
      {
        _AdpressoIntersitial_Show();
      }

      [DllImport("__Internal")]
    private static extern void _AdpressoIntersitial_Cancel();
      public override void Cancel()
      {
        _AdpressoIntersitial_Cancel();
      }

    }

#elif UNITY_ANDROID

  public class AdpressoInterstitialNativeAndroid : AdpressoInterstitialNative
  {
	private AndroidJavaClass AdpressoUnityBridgeClass =  new AndroidJavaClass("com.adpresso.android.unity.InterstitialUnityBridge");
    
    public static AndroidJavaObject getCurrentActivity() {
      AndroidJavaClass unityPlayer = new AndroidJavaClass("com.unity3d.player.UnityPlayer");
      AndroidJavaObject unityActivity = unityPlayer.GetStatic<AndroidJavaObject>("currentActivity");
      
      return unityActivity;
    }

    public AdpressoInterstitialNativeAndroid(string publisherId, string callbackName)
    {
      AndroidJavaObject unityActivity = getCurrentActivity();
      AdpressoUnityBridgeClass.CallStatic("initialize", unityActivity, publisherId, callbackName); 
    }
    
    
  
    static bool IsEmulator()
    {
      return Application.platform != RuntimePlatform.Android;
    }
  

    public override void Show()
    {
      AdpressoUnityBridgeClass.CallStatic("show");
    }
    
  }

#endif

}
