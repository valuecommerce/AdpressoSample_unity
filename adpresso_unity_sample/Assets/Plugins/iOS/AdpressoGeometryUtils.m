//
//  AdpressoGeometryUtils.m
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

#import "AdpressoGeometryUtils.h"

///////////////////////////////////////////////////////////////////////////////////////////////////
CGRect ADLRectFromRectSubtractingRect(CGRect baseRect, CGRect subRect)
{
  if (CGRectIsEmpty(subRect) || !CGRectIntersectsRect(baseRect, subRect)) {
    return baseRect;
  }
  
  CGRect intersectRect = CGRectIntersection(baseRect, subRect);
  
  // is intersect rect all of base rect, if so exit with empty rect
  if (CGRectEqualToRect(baseRect, intersectRect)) {
    return CGRectZero;
  }
  
  if (CGRectGetMinY(intersectRect) <= CGRectGetMinY(baseRect) && CGRectGetMaxY(intersectRect) >= CGRectGetMaxY(baseRect)) {
    if (CGRectGetMaxX(intersectRect) < CGRectGetMaxX(baseRect)) {
      // left
      return CGRectMake(CGRectGetMaxX(intersectRect), baseRect.origin.y, CGRectGetMaxX(baseRect) - CGRectGetMaxX(intersectRect), baseRect.size.height);
    }
    else if (CGRectGetMinX(intersectRect) > CGRectGetMinX(baseRect)) {
      // right
      return CGRectMake(baseRect.origin.x, baseRect.origin.y, CGRectGetMinX(intersectRect) - CGRectGetMinX(baseRect), baseRect.size.height);
    }
  }
  else if (CGRectGetMinX(intersectRect) <= CGRectGetMinX(baseRect) && CGRectGetMaxX(intersectRect) >= CGRectGetMaxX(baseRect)) {
    if (CGRectGetMaxY(intersectRect) < CGRectGetMaxY(baseRect)) {
      // bottom
      return CGRectMake(baseRect.origin.x, CGRectGetMaxY(intersectRect), baseRect.size.width, CGRectGetMaxY(baseRect) - CGRectGetMaxY(intersectRect));
    }
    else if (CGRectGetMinY(intersectRect) > CGRectGetMinY(baseRect)) {
      // top 
      return CGRectMake(baseRect.origin.x, baseRect.origin.y, baseRect.size.width, CGRectGetMinY(intersectRect) - CGRectGetMinY(baseRect));
    }
  }
  
  return baseRect;
}

///////////////////////////////////////////////////////////////////////////////////////////////////
// convert status bar to view coordinates
// result is only valid when view is attached to window
CGRect ADLConvertStatusBarFrameToViewRect(UIView* view) 
{
  CGRect statusBarFrame = [[UIApplication sharedApplication] statusBarFrame];
  
  CGRect statusBarWindowRect = statusBarFrame;
  
  if (view.window) {
    statusBarWindowRect = [view.window convertRect:statusBarFrame fromWindow: nil];
  }
  
  CGRect statusBarViewRect = [view convertRect:statusBarWindowRect fromView:nil];
  
  return statusBarViewRect;
}

