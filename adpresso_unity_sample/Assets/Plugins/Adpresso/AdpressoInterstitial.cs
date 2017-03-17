//
//  AdpressoInterstitial
//  Adpresso SDK
//
//  Copyright 2014 Glossom, inc. All rights reserved.
//
//
using UnityEngine;
using System.Collections;
using Adpresso.AdSdk;

public class AdpressoInterstitial : MonoBehaviour {
  // 
  // 下記の行をコメントアウトして、管理画面へ表示されたinterstitial広告用の広告枠コードをコピーして下さい。
  // 
  public string publisherId = "Mjc3NzA%3D%0A";

  // Use this for initialization
  void Start () {
    AdpressoInterstitialNative.initWithPublisherId(this.publisherId, gameObject.name);
    AdpressoInterstitialNative.Instance.Show();
  }
  
  // Update is called once per frame
  // void Update () {
  // 
  // }

  public void interstitialAdRequestComplete(string msg)
  {
    Debug.Log("[unity]interstitialAdRequestComplete");
  }
  
  public void interstitialAdRequestFailed(string msg)
  {
    Debug.Log("[unity]interstitialAdRequestFailed");
  }
  public void interstitialAdWillBePresented(string msg)
  {
    Debug.Log("[unity]interstitialAdWillBePresented");
  }
  public void interstitialAdWasDismissed(string msg)
  {
    Debug.Log("[unity]interstitialAdWasDismissed");
  }
}
