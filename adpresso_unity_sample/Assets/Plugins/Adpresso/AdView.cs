//
//  AdView
//  Adpresso SDK
//
//  Copyright 2014 Glossom, inc. All rights reserved.
//
//

using UnityEngine;
using System.Collections;

using Adpresso.AdSdk;

public class AdView : MonoBehaviour {
  // 
  // 下記の行をコメントアウトして、管理画面へ表示されたバナー広告用の広告枠コードをコピーして下さい。
  // 
  public string publisherId = "MTM5NjM%3D";
  public AdViewNative.Position position = AdViewNative.Position.Top;

  void Start() {
    _log("AdView.Start");
    _log("object name:" + gameObject.name);
    AdViewNative.Instance.SetPublisherId(this.publisherId);
    AdViewNative.Instance.SetPosition(position);
    AdViewNative.Instance.Show();

  }
  
  public void _log(string s) {
    AdViewNative.Instance.Log(s);
  }
  
}
