//
//  AdpressoView.h
//  AdLantis iOS SDK
//
//  Copyright 2009-2014 Atlantiss.jp. All rights reserved.
//  Copyright 2016 valuecommerce All rights reserved.
//

#import <UIKit/UIKit.h>

///////////////////////////////////////////////////////////////////////////////////////////////////
typedef NS_ENUM(NSUInteger, AdlantisViewTransition) {
  AdpressoViewTransitionFadeIn,
  AdpressoViewTransitionSlideFromRight,
  AdpressoViewTransitionSlideFromLeft,
  AdpressoViewTransitionNone
};

@protocol AdlantisViewDelegate;
@class AdpressoTargetingParameters;

///////////////////////////////////////////////////////////////////////////////////////////////////
@interface AdpressoView : UIView

@property (nonatomic,strong)
#if __IPHONE_OS_VERSION_MAX_ALLOWED >= 80000
IBInspectable
#endif
NSString *publisherID;

@property (nonatomic,weak) id<AdlantisViewDelegate> delegate;

@property (nonatomic,assign) AdlantisViewTransition defaultTransition;

// amount of time (in seconds) before fetching next set of ads, set to zero to stop ad fetch
@property (nonatomic,assign) NSTimeInterval adFetchInterval;

// amount of time (in seconds) before showing the next ad
@property (nonatomic,assign) NSTimeInterval adDisplayInterval;

@property (nonatomic,weak) UIViewController *rootViewController;

@property (nonatomic,strong) AdpressoTargetingParameters *targetingParameters;

- (IBAction)showNextAd:(id)sender;
- (IBAction)showPreviousAd:(id)sender;

@property (nonatomic,readonly) BOOL collapsed;
- (IBAction)collapse;
- (IBAction)uncollapse;
- (IBAction)toggleCollapse;

- (IBAction)fadeIn;
- (IBAction)fadeOut;
- (IBAction)toggleFaded;

- (void)requestAds;

@property (nonatomic,readonly) UIInterfaceOrientation aspectOrientation DEPRECATED_ATTRIBUTE; // the orientation for which ads are shown

+ (CGSize)sizeForOrientation:(UIInterfaceOrientation)orientation   DEPRECATED_MSG_ATTRIBUTE("use the AdpressoViewSize function");

@end

///////////////////////////////////////////////////////////////////////////////////////////////////

@protocol AdlantisViewDelegate <NSObject>

- (void)bannerAdRequestComplete:(AdpressoView*)adView;

- (void)bannerAdRequestFailed:(AdpressoView*)adView;

@optional

// The bannerAdPreview methods are only used for mediation when the mediated ad shows a preview.
- (void)bannerAdPreviewWillBeShown:(AdpressoView*)adView;

- (void)bannerAdPreviewWillBeHidden:(AdpressoView*)adView;

- (void)bannerAdTouched:(AdpressoView*)adView;

@end

///////////////////////////////////////////////////////////////////////////////////////////////////
typedef NS_ENUM(NSUInteger, AdlantisViewLocation) {
  AdpressoViewLocationAtTop = 0,
  AdpressoViewLocationAtBottom,
  AdpressoViewLocationElsewhere,
};

///////////////////////////////////////////////////////////////////////////////////////////////////
#ifdef __cplusplus
extern "C" {
#endif
  CGSize AdpressoViewSize();
  AdlantisViewLocation AdpressoLocationForView(UIView *view);
  
  CGSize AdpressoViewSizeForOrientation(UIInterfaceOrientation orientation)   DEPRECATED_MSG_ATTRIBUTE("use the AdpressoViewSize function");

#ifdef __cplusplus
} /* closing brace for extern "C" */
#endif

