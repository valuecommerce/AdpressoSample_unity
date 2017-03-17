//
//  AdpressoGeometryUtils.h
//
//  Created on 6/24/11.
//  Copyright 2011 Atlantis Co., Inc.
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

// #import <Foundation/Foundation.h>

#ifdef __cplusplus
extern "C" {
#endif

// if subrect includes an entire edge of baseRect, then determine remaining rect in baseRect that doesn't include subRect
CGRect ADLRectFromRectSubtractingRect(CGRect baseRect, CGRect subRect);

CGRect ADLConvertStatusBarFrameToViewRect(UIView* view);
  
#ifdef __cplusplus
} /* closing brace for extern "C" */
#endif
