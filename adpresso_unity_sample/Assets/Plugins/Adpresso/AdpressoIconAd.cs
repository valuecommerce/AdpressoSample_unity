using UnityEngine;
using System.Collections;
using Adpresso.AdSdk;

public class AdpressoIconAd : MonoBehaviour {
  // 
  // 下記の行をコメントアウトして、管理画面へ表示されたicon広告用の広告枠コードをコピーして下さい。
  // 
  public string publisherId = "Mjc3NzE%3D%0A";
  public AdpressoIconNative.IconAttr[] icons;

  // Use this for initialization
  void Start () {
    AdpressoIconNative.initWithPublisherId(this.publisherId, gameObject.name);
    AdpressoIconNative.Instance.Load(icons);

  }
  
  // Update is called once per frame
  // void Update () {
  // 
  // }
  
  void iconAdRequestComplete(string msg)
  {
    
  }
  
  void iconAdRequestFailed(string msg)
  {
  }
}
