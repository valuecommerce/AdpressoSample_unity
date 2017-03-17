//
//  AdpressoSDKBinding.mm
//  Adpresso SDK
//
//  Copyright 2014 Glossom, inc. All rights reserved.
//
//

#import "AdpressoSDKBinding.h"
#import "AdpressoView.h"
#import "AdpressoAdManager.h"

#import "AdpressoGeometryUtils.h"

//#define GREE_SDK_SUPPORT

#import "UnityInterface.h"

AdpressoView *AdView();
UIInterfaceOrientation AdView_CurrentOrientation();
UIInterfaceOrientation AdView_OrientationForPositionAndOrientation(AdViewPosition position, UIInterfaceOrientation orientation);

///////////////////////////////////////////////////////////////////////////////////////////////////
@interface AdViewHelper() <AdlantisViewDelegate>
@end

///////////////////////////////////////////////////////////////////////////////////////////////////
@implementation AdViewHelper

///////////////////////////////////////////////////////////////////////////////////////////////////
- (instancetype)init 
{
  self = [super init];
  if (self) {
    CGSize suggestedViewSize = [[AdpressoView class] sizeForOrientation: UIApplication.sharedApplication.statusBarOrientation];
    CGRect adViewFrame = CGRectMake(0, 0, suggestedViewSize.width, suggestedViewSize.height);
    _adView = [[AdpressoView alloc] initWithFrame: adViewFrame];
    
    if ([_adView respondsToSelector:@selector(setDelegate:)]) {
      ((AdpressoView*)_adView).delegate = self;
    }
  }
  return self;
}

///////////////////////////////////////////////////////////////////////////////////////////////////
- (instancetype)initWithAdView:(UIView*)inAdView 
{
  self = [super init];
  if (self) {
    self.adView = inAdView;
    if ([_adView respondsToSelector:@selector(setDelegate:)]) {
      ((AdpressoView*)_adView).delegate = self;
    }
  }
  
  return self;
}

///////////////////////////////////////////////////////////////////////////////////////////////////
- (void)dealloc 
{
  [_adView removeFromSuperview];
  
//  [_adView release];

//  [super dealloc];
}

///////////////////////////////////////////////////////////////////////////////////////////////////
- (void)setPublisherId:(NSString*)publisherId
{
  if ([_adView respondsToSelector:@selector(setPublisherID:)]) {
    ((AdpressoView*)_adView).publisherID = publisherId;
  }
}

///////////////////////////////////////////////////////////////////////////////////////////////////
- (void)setPosition:(AdViewPosition)inPosition forOrientation:(UIInterfaceOrientation)orientation
{
  _position = inPosition;
  
  UIView *sharedContainer = _adView.superview;
  CGRect containerBounds = ADLUseableRectForView(sharedContainer, _adView);
  
  CGSize suggestedViewSize = [[AdpressoView class] sizeForOrientation: AdView_OrientationForPositionAndOrientation(_position, orientation)];
  _adView.transform = CGAffineTransformIdentity;
  _adView.frame = CGRectMake(0, 0, suggestedViewSize.width, suggestedViewSize.height);
  
  switch (_position) {
      
    case AdViewTop:
      _adView.frame = CGRectMake(containerBounds.origin.x + (containerBounds.size.width - suggestedViewSize.width) / 2,
                                 containerBounds.origin.y, suggestedViewSize.width, suggestedViewSize.height);
      break;
      
    case AdViewBottom:
      _adView.frame = CGRectMake(containerBounds.origin.x + (containerBounds.size.width - suggestedViewSize.width) / 2,
                                 containerBounds.origin.y + containerBounds.size.height - suggestedViewSize.height,
                                 suggestedViewSize.width, suggestedViewSize.height);
      break;
      
    case AdViewLeft:
      // unsupported
      break;
      
    case AdViewRight:
      // unsupported
      break;
  }
}

///////////////////////////////////////////////////////////////////////////////////////////////////
- (void)setPosition:(AdViewPosition)inPosition
{
  [self setPosition:inPosition forOrientation: AdView_CurrentOrientation()];
}

///////////////////////////////////////////////////////////////////////////////////////////////////
- (void)resetPosition
{
  [self setPosition: _position];
}

///////////////////////////////////////////////////////////////////////////////////////////////////
- (void)repositionForOrientationTo:(UIInterfaceOrientation)toInterfaceOrientation
{
  CGSize suggestedViewSize = [[AdpressoView class] sizeForOrientation: toInterfaceOrientation];
  
  CGRect tempRect = _adView.frame;
  tempRect.size = suggestedViewSize;
  
  UIView *container = _adView.superview;
  
  if (_position == AdViewBottom && container) {
    unsigned containerHeight = UIInterfaceOrientationIsLandscape(toInterfaceOrientation) ? CGRectGetHeight(container.frame) : CGRectGetWidth(container.frame);
    
    tempRect.origin.y = containerHeight - suggestedViewSize.height;
  }
  
  GetAdViewHelper().adView.frame = tempRect;
}

#pragma mark - AdlantisViewDelegate methods

- (void)bannerAdRequestComplete:(AdpressoView*)adView
{
}

- (void)bannerAdRequestFailed:(AdpressoView*)adView
{
}

- (void)bannerAdPreviewWillBeShown:(AdpressoView*)adView
{
  UnityPause(true);
}

- (void)bannerAdPreviewWillBeHidden:(AdpressoView*)adView
{
  UnityPause(false);
}

- (void)bannerAdTouched:(AdpressoView*)adView
{
}

@end

static AdViewHelper *gAdViewHelper = nil;

///////////////////////////////////////////////////////////////////////////////////////////////////
AdViewHelper* AdViewHelper_Init()
{
  if (gAdViewHelper == nil) {
    AdViewHelper *adViewHelper = [[AdViewHelper alloc] init];
    
    AdViewHelper_Set(adViewHelper);
  }
  
  return gAdViewHelper;
}

///////////////////////////////////////////////////////////////////////////////////////////////////
void AdViewHelper_Set(AdViewHelper *adViewHelper) 
{
  gAdViewHelper = adViewHelper;
//  [gAdViewHelper release];
  
//  gAdViewHelper = [adViewHelper retain];
}

///////////////////////////////////////////////////////////////////////////////////////////////////
void _AdView_SetPublisherId(char * inPublisherId) 
{
  //NSLog(@"%s", __PRETTY_FUNCTION__);
  [gAdViewHelper setPublisherId:@(inPublisherId)];
}

///////////////////////////////////////////////////////////////////////////////////////////////////
void _AdView_SetGapPublisherId(char * inPublisherId) 
{
#ifdef GREE_SDK_SUPPORT
  //NSLog(@"%s", __PRETTY_FUNCTION__);
  [gAdViewHelper setPublisherId:@(inPublisherId)];
#endif
}

///////////////////////////////////////////////////////////////////////////////////////////////////
AdViewHelper* GetAdViewHelper() 
{
  return gAdViewHelper;
}

///////////////////////////////////////////////////////////////////////////////////////////////////
AdpressoView *AdView() 
{
  return (AdpressoView*)gAdViewHelper.adView;
}

///////////////////////////////////////////////////////////////////////////////////////////////////
void _AdView_Init()
{
  AdViewHelper_Init();
}

///////////////////////////////////////////////////////////////////////////////////////////////////
void _AdView_ShowHide(bool show)
{
  if (AdView() == nil) {
    AdViewHelper_Init();
  }
  
  if (AdView().superview == NULL) {
    UIView *rootView = UnityGetGLView();
    [rootView addSubview:AdView()];
  }
  
  [GetAdViewHelper() resetPosition];
  [AdView() setHidden:!show];
}

///////////////////////////////////////////////////////////////////////////////////////////////////
void _AdView_FadeIn() {
  [AdView() fadeIn];
}

///////////////////////////////////////////////////////////////////////////////////////////////////
void _AdView_FadeOut() {
  [AdView() fadeOut];
}

///////////////////////////////////////////////////////////////////////////////////////////////////
UIInterfaceOrientation AdView_CurrentOrientation() 
{
  return UIApplication.sharedApplication.statusBarOrientation;
}

///////////////////////////////////////////////////////////////////////////////////////////////////
UIInterfaceOrientation AdView_OrientationForPositionAndOrientation(AdViewPosition position, UIInterfaceOrientation orientation)
{
  switch (position) {
    case AdViewTop:
    case AdViewBottom:
    default:
      return orientation;
      break;
      
    case AdViewLeft:
    case AdViewRight:
      if (UIInterfaceOrientationIsPortrait(orientation)) {
        return UIInterfaceOrientationLandscapeRight;
      }
      else {
        return UIInterfaceOrientationPortrait;
      }
      break;
  }
}

///////////////////////////////////////////////////////////////////////////////////////////////////
UIInterfaceOrientation AdView_OrientationForPosition(AdViewPosition position)
{
  return AdView_OrientationForPositionAndOrientation(position, AdView_CurrentOrientation());
}

///////////////////////////////////////////////////////////////////////////////////////////////////
CGRect ADLUseableRectForView(UIView *containerView, UIView *subview)
{
  CGRect containerBounds = containerView.bounds;
  
  if (![[UIApplication sharedApplication] isStatusBarHidden] && subview.window) {
    CGRect statusBarViewRect = ADLConvertStatusBarFrameToViewRect(subview.superview);
    containerBounds = ADLRectFromRectSubtractingRect(containerBounds, statusBarViewRect);
  }
  
  // avoid other subviews of the superview
  for (UIView* siblingView in containerView.subviews) {
    if (siblingView != subview && !siblingView.hidden) {
      CGRect subviewFrame = [siblingView convertRect:siblingView.bounds toView:containerView];
      containerBounds = ADLRectFromRectSubtractingRect(containerBounds, subviewFrame);
    }
  }
  
  return containerBounds;
}

///////////////////////////////////////////////////////////////////////////////////////////////////
void _AdView_SetPosition(AdViewPosition position)
{
  [GetAdViewHelper() setPosition:position];
}

///////////////////////////////////////////////////////////////////////////////////////////////////
void _AdView_Log(char* s) {
  NSLog(@"%@", @(s));
}
