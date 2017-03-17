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

using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using UnityEditor;

public class MobileBuildScript : EditorWindow {
  
  static string[] GetEnabledScenePaths()
  {
    List<string> enabledScenes = new List<string>();
    
    foreach (EditorBuildSettingsScene scene in EditorBuildSettings.scenes) 
    {
        if (scene.enabled)
        {
          enabledScenes.Add(scene.path);
        }
    }
    
    return enabledScenes.ToArray();
  }
  
  [MenuItem("Tools/Build iOS")]
  static void PerformIosBuild()
  {
    PerformBuild(BuildTarget.iOS, "ios_project");
  }
  
  [MenuItem("Tools/Build Android")]
  static void PerformAndroidBuild()
  {
    PerformBuild(BuildTarget.Android, "android_project.apk");
  }
  
  static void PerformBuild(BuildTarget platform, string projectName)
  {
    EditorUserBuildSettings.SwitchActiveBuildTarget(platform);
    
    System.Console.WriteLine("MobileBuildScript:PerformBuild: " + projectName);
    
    BuildPipeline.BuildPlayer(GetEnabledScenePaths(), projectName, platform, BuildOptions.None);

    System.Console.WriteLine("MobileBuildScript:PerformBuild - Finished");
  }
  
}
