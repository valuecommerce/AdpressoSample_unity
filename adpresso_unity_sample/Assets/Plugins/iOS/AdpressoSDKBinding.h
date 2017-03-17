//
//  AdpressoSDKBinding.h
//  Adpresso SDK
//
//  Copyright 2014 Glossom, inc. All rights reserved.
//
//


#ifdef __cplusplus
extern "C" {
#endif

typedef enum {
  AdViewTop,
  AdViewBottom,
  AdViewLeft,
  AdViewRight,
} AdViewPosition;
  
#ifdef __OBJC__

///////////////////////////////////////////////////////////////////////////////////////////////////
@interface AdViewHelper : NSObject

@property (nonatomic, retain) UIView *adView;
@property (nonatomic) AdViewPosition position;

- (id)initWithAdView:(UIView*)inAdView;

- (void)setPosition:(AdViewPosition)inPosition forOrientation:(UIInterfaceOrientation)orientation;

- (void)resetPosition;

- (void)repositionForOrientationTo:(UIInterfaceOrientation)toInterfaceOrientation;

@end
  
void AdViewHelper_Set(AdViewHelper *adViewHelper);
  
AdViewHelper* AdViewHelper_Init();
AdViewHelper* GetAdViewHelper();
  
#endif
  
CGRect ADLUseableRectForView(UIView *containerView, UIView *subview);

void _AdView_Init();
void _AdView_SetPublisherId(char * inPublisherId);
void _AdView_SetGapPublisherId(char * inPublisherId);

void _AdView_ShowHide(bool show);
void _AdView_Collapse(bool collapse);
void _AdView_FadeIn();
void _AdView_FadeOut();
  
void _AdView_SetPosition(AdViewPosition position);

void _AdView_Log(char* s);
  
#ifdef __cplusplus
} /* closing brace for extern "C" */
#endif

