//
// Adpresso Plugin
// AdViewTest
//
// Copyright 2011-2012 Atlantis Co., Ltd.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//    http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//

using UnityEngine;
using System.Collections;

using Adpresso.AdSdk;

public class AdpressoTest : MonoBehaviour {
  
  ScreenOrientation currentOrientation;
  AdViewNative.Position bannerAdPosition;
  
  void Start() {
    print("AdpressoTest.Start");
    currentOrientation = Screen.orientation;
    SetBannerPosition(AdViewNative.Position.Top);
  }
  
  void OnGUI() {
    ResetButton();

    if(MakeButton("Show")) {
      AdViewNative.Instance.Show();
    }

    if(MakeButton("Hide")) {
      AdViewNative.Instance.Hide();
    }

    if(MakeButton("Fade In")) {
      AdViewNative.Instance.FadeIn();
    }

    if(MakeButton("Fade Out")) {
      AdViewNative.Instance.FadeOut();
    }

    if (MakeButton("Top")) {
      SetBannerPosition(AdViewNative.Position.Top);
    }

    if (MakeButton("Bottom")) {
      SetBannerPosition(AdViewNative.Position.Bottom);
    }

    if(MakeButton("IS Show")) {
      AdpressoInterstitialNative.Instance.Show();
    }

    if(MakeButton(" Icon Show")) {
      AdpressoIconNative.Instance.Show();
    }
    if(MakeButton(" Icon Hide")) {
      AdpressoIconNative.Instance.Hide();
    }
  }
  
  void SetBannerPosition(AdViewNative.Position inBannerPosition)
  {
    bannerAdPosition = inBannerPosition;
    UpdateBannerPosition();
  }
  
  void UpdateBannerPosition()
  {
    AdViewNative.Instance.SetPosition(bannerAdPosition);
  }

  // code adapted from GREE SDK
  int buttonX = 0;
  int buttonY = 0;
  
  static int adMaxHeight = 50;
  
  void ResetButton(){
    buttonX = 0;
    buttonY = 0;
  }
  
  int ButtonColumns(){
    return 3;
  }
  
  int ButtonWidth(){
    return (Screen.width - ButtonOffsetX() * 2) /  ButtonColumns() - ButtonGapWidth();
  }
  
  int ButtonHeight(){
    return 60;
  }
  
  int ButtonGapWidth(){
    return 5;
  }
  
  int ButtonGapHeight(){
    return 5;
  }
  
  int ButtonOffsetX() {
    if (Screen.width > 320) {
      return (adMaxHeight * 2) + 5;
    }
    else {
      return adMaxHeight + 5;
    }
  }
  
  int ButtonOffsetY() {
    return 80;
  }
  
  Rect ButtonRect(int _buttonX, int _buttonY) {
    return new Rect(ButtonOffsetX() + _buttonX * (ButtonWidth() + ButtonGapWidth()),
      ButtonOffsetY() + _buttonY * (ButtonHeight() + ButtonGapHeight()),
      ButtonWidth(), ButtonHeight());
  }
  
  bool MakeButton(string label) {
    
    bool b = GUI.Button(ButtonRect(buttonX, buttonY), label);
    
    buttonX++;
    if(buttonX == ButtonColumns()){
      buttonX = 0;
      buttonY++;
    }

    return b;
  }
  
  void Update() {
    // print("AdpressoTest.Update");
    
    if (Screen.orientation != currentOrientation) {
      print("AdpressoTest orientationChanged");
      
      currentOrientation = Screen.orientation;
      
      UpdateBannerPosition();
    }
  }
  
}
