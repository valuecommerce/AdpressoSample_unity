//
//  AdpressoIconNative
//  Adpresso SDK
//
//  Copyright 2014 Glossom, inc. All rights reserved.
//
//
#define USE_ADVIEW_IOS_NATIVE

using UnityEngine;
using System.Runtime.InteropServices;
using System;
using System.Collections;

namespace Adpresso.AdSdk
{
    public class AdpressoIconNative
    {
        [System.Serializable]
        public class Position
        {
          public float x;
          
          public float y;
          
          public Position(float x, float y)
          {
            this.x = x;
            this.y = y;
          }
        }

        [System.Serializable]
        public class IconAttr
        {
          public Position position;
          public bool showText;
          public Color textColor = Color.black;
        }

        public struct PointF
        {
          public float x;
      
          public float y;
      
          public PointF(float px, float py)
          {
            x = px;
            y = py;
          }
        }
        
        private static AdpressoIconNative instance;
        
        public static AdpressoIconNative Instance
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
            instance = new AdpressoIconNative();
          #elif UNITY_IPHONE && USE_ADVIEW_IOS_NATIVE
            instance = new AdpressoIconNative();
          #elif UNITY_ANDROID
            instance = new AdpressoIconNativeAndroid(publisherId, callbackName);
          #endif
        } 
        
        public void Load(IconAttr[] icons)
        {
          foreach(IconAttr icon in icons)
          {
            Add(icon);
          }
          Load();
        }
        
        public virtual void Add(IconAttr icon)
        {
        }
        
        public virtual void Remove(IconAttr icon) 
        {
        }
        
        public virtual void Load()
        {
        }
        
        public virtual void Show()
        {

        }
        public virtual void Hide()
        {
          
        }
        
        public virtual void Log(string s)
        {
        }

    }
    
#if UNITY_ANDROID

  public class AdpressoIconNativeAndroid : AdpressoIconNative
  {
    private AndroidJavaClass AdpressoUnityBridgeClass =  new AndroidJavaClass("com.adpresso.android.unity.IconUnityBridge");
    
    public static AndroidJavaObject getCurrentActivity() {
      AndroidJavaClass unityPlayer = new AndroidJavaClass("com.unity3d.player.UnityPlayer");
      AndroidJavaObject unityActivity = unityPlayer.GetStatic<AndroidJavaObject>("currentActivity");
      
      return unityActivity;
    }
      
    public AdpressoIconNativeAndroid(string publisherId, string callbackName)
    {
      AndroidJavaObject unityActivity = getCurrentActivity();
      AdpressoUnityBridgeClass.CallStatic("initialize", unityActivity, publisherId, callbackName);
    }
    
    static bool IsEmulator()
    {
      return Application.platform != RuntimePlatform.Android;
    }
    
    public override void Add(IconAttr icon)
    {
      AndroidJavaObject unityActivity = getCurrentActivity();
      AdpressoUnityBridgeClass.CallStatic("add", unityActivity, icon.position.x, icon.position.y, icon.showText,(int)(icon.textColor.r * 255), (int)(icon.textColor.g * 255), (int)(icon.textColor.b * 255));
    }

    public void setTextColor(IconAttr icon){
      AndroidJavaObject unityActivity = getCurrentActivity();
      AdpressoUnityBridgeClass.CallStatic("setTextColor", unityActivity, icon.position.x, icon.position.y, (int)(icon.textColor.r * 255), (int)(icon.textColor.g * 255), (int)(icon.textColor.b * 255));
    }
    public override void Remove(IconAttr icon)
    {
      AndroidJavaObject unityActivity = getCurrentActivity();
      AdpressoUnityBridgeClass.CallStatic("remove", unityActivity, icon.position.x, icon.position.y);
    }
    
    public override void Load()
    {
      AndroidJavaObject unityActivity = getCurrentActivity();
      AdpressoUnityBridgeClass.CallStatic("load", unityActivity);
    }

    public enum Visibility : int {
      VISIBLE = 0,
      INVISIBLE = 4,
      GONE = 8
    }
  
    public void SetVisibility(Visibility visibility)
    {
      AdpressoUnityBridgeClass.CallStatic("setViewVisibility", (int)visibility);
    }
    
    public override void Show()
    {
      SetVisibility(Visibility.VISIBLE);
    }
  
    public override void Hide()
    {
      SetVisibility(Visibility.INVISIBLE);
    }
  }

#endif

}
