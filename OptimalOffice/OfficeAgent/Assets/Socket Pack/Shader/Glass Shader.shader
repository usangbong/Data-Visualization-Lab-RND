Shader "NatureManufacture Shaders/Standard Metalic Glass"
{
	Properties
	{
		[HideInInspector] __dirty( "", Int ) = 1
		_Albedo("Albedo", 2D) = "white" {}
		_Normal("Normal", 2D) = "bump" {}
		_MetalicRAmbientOcclusionGSmoothnessA("Metalic (R) Ambient Occlusion (G) Smoothness (A)", 2D) = "white" {}
		_SmoothnessPower("Smoothness Power", Range( 0 , 2)) = 1
		_GlassNormal("Glass Normal", 2D) = "bump" {}
		_Distortion("Distortion", Range( 0 , 1)) = 0.292
		[HideInInspector] _texcoord( "", 2D ) = "white" {}
		[Header(Translucency)]
		_Translucency("Strength", Range( 0 , 50)) = 1
		_TransNormalDistortion("Normal Distortion", Range( 0 , 1)) = 0.1
		_TransScattering("Scaterring Falloff", Range( 1 , 50)) = 2
		_TransDirect("Direct", Range( 0 , 1)) = 1
		_TransAmbient("Ambient", Range( 0 , 1)) = 0.2
		_TransShadow("Shadow", Range( 0 , 1)) = 0.9
	}

	SubShader
	{
		Tags{ "RenderType" = "Opaque"  "Queue" = "Geometry+0" "IsEmissive" = "true"  }
		Cull Off
		GrabPass{ "_ScreenGrab0" }
		CGPROGRAM
		#include "UnityPBSLighting.cginc"
		#pragma target 3.0
		#pragma surface surf StandardCustom keepalpha  
		struct Input
		{
			float2 uv_texcoord;
			float4 screenPos;
		};

		struct SurfaceOutputStandardCustom
		{
			fixed3 Albedo;
			fixed3 Normal;
			half3 Emission;
			half Metallic;
			half Smoothness;
			half Occlusion;
			fixed Alpha;
			fixed3 Translucency;
		};

		uniform sampler2D _Normal;
		uniform float4 _Normal_ST;
		uniform sampler2D _Albedo;
		uniform float4 _Albedo_ST;
		uniform sampler2D _ScreenGrab0;
		uniform sampler2D _GlassNormal;
		uniform float4 _GlassNormal_ST;
		uniform float _Distortion;
		uniform sampler2D _MetalicRAmbientOcclusionGSmoothnessA;
		uniform float4 _MetalicRAmbientOcclusionGSmoothnessA_ST;
		uniform float _SmoothnessPower;
		uniform half _Translucency;
		uniform half _TransNormalDistortion;
		uniform half _TransScattering;
		uniform half _TransDirect;
		uniform half _TransAmbient;
		uniform half _TransShadow;

		inline half4 LightingStandardCustom(SurfaceOutputStandardCustom s, half3 viewDir, UnityGI gi )
		{
			#if !DIRECTIONAL
			float3 lightAtten = gi.light.color;
			#else
			float3 lightAtten = lerp( _LightColor0, gi.light.color, _TransShadow );
			#endif
			half3 lightDir = gi.light.dir + s.Normal * _TransNormalDistortion;
			half transVdotL = pow( saturate( dot( viewDir, -lightDir ) ), _TransScattering );
			half3 translucency = lightAtten * (transVdotL * _TransDirect + gi.indirect.diffuse * _TransAmbient) * s.Translucency;
			half4 c = half4( s.Albedo * translucency * _Translucency, 0 );

			SurfaceOutputStandard r;
			r.Albedo = s.Albedo;
			r.Normal = s.Normal;
			r.Emission = s.Emission;
			r.Metallic = s.Metallic;
			r.Smoothness = s.Smoothness;
			r.Occlusion = s.Occlusion;
			r.Alpha = s.Alpha;
			return LightingStandard (r, viewDir, gi) + c;
		}

		inline void LightingStandardCustom_GI(SurfaceOutputStandardCustom s, UnityGIInput data, inout UnityGI gi )
		{
			UNITY_GI(gi, s, data);
		}

		void surf( Input i , inout SurfaceOutputStandardCustom o )
		{
			float2 uv_Normal = i.uv_texcoord * _Normal_ST.xy + _Normal_ST.zw;
			o.Normal = UnpackNormal( tex2D( _Normal,uv_Normal) );
			float2 uv_Albedo = i.uv_texcoord * _Albedo_ST.xy + _Albedo_ST.zw;
			float4 tex2DNode40 = tex2D( _Albedo,uv_Albedo);
			o.Albedo = tex2DNode40.rgb;
			float4 screenPos4 = i.screenPos;
			screenPos4.w += 0.00000000001;
			screenPos4.xyzw /= screenPos4.w;
			float2 componentMask39 = screenPos4.xy;
			float2 uv_GlassNormal = i.uv_texcoord * _GlassNormal_ST.xy + _GlassNormal_ST.zw;
			float2 componentMask36 = ( UnpackNormal( tex2D( _GlassNormal,uv_GlassNormal) ) * _Distortion ).xy;
			o.Emission = ( tex2DNode40 * tex2D( _ScreenGrab0, ( componentMask39 + componentMask36 ) ) ).rgb;
			float2 uv_MetalicRAmbientOcclusionGSmoothnessA = i.uv_texcoord * _MetalicRAmbientOcclusionGSmoothnessA_ST.xy + _MetalicRAmbientOcclusionGSmoothnessA_ST.zw;
			float4 tex2DNode41 = tex2D( _MetalicRAmbientOcclusionGSmoothnessA,uv_MetalicRAmbientOcclusionGSmoothnessA);
			o.Metallic = tex2DNode41.r;
			o.Smoothness = ( tex2DNode41.a * _SmoothnessPower );
			o.Occlusion = tex2DNode41.g;
			o.Translucency = tex2DNode40.rgb;
			o.Alpha = 1;
		}

		ENDCG
	}
}
