#!/usr/bin/env python3
"""
Supply Chain Data Analysis Generator
Analyzes the enhanced grocery dataset to generate real supply chain insights and challenges
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime
import json

class SupplyChainDataAnalyzer:
    def __init__(self, dataset_path: str):
        self.dataset_path = dataset_path
        self.df = None
        self.insights = {}
        
    def load_data(self):
        """Load the enhanced dataset"""
        print("Loading enhanced grocery dataset...")
        self.df = pd.read_csv(self.dataset_path)
        print(f"Loaded {len(self.df):,} transactions with {len(self.df.columns)} columns")
        
    def analyze_demand_forecasting(self):
        """Analyze demand forecasting challenges"""
        print("Analyzing demand forecasting...")
        
        # Forecast accuracy analysis
        forecast_stats = self.df['forecast_accuracy'].describe()
        avg_accuracy = forecast_stats['mean']
        
        # Demand volatility analysis
        volatility_stats = self.df['demand_volatility'].describe()
        avg_volatility = volatility_stats['mean']
        
        # Weather impact analysis
        weather_impact = self.df.groupby('weather_condition')['weather_impact_score'].mean()
        
        # Seasonal analysis
        seasonal_demand = self.df.groupby('season')['seasonal_demand_factor'].mean()
        
        # Category-wise forecast accuracy
        category_accuracy = self.df.groupby('category')['forecast_accuracy'].mean().sort_values(ascending=False)
        
        self.insights['demand_forecasting'] = {
            'average_accuracy': round(avg_accuracy, 1),
            'average_volatility': round(avg_volatility, 3),
            'weather_impact': weather_impact.to_dict(),
            'seasonal_demand': seasonal_demand.to_dict(),
            'category_accuracy': category_accuracy.to_dict(),
            'challenges': {
                'low_accuracy_categories': category_accuracy[category_accuracy < 75].to_dict(),
                'high_volatility_items': len(self.df[self.df['demand_volatility'] > 0.5]),
                'weather_sensitive_items': len(self.df[self.df['weather_impact_score'] > 80])
            }
        }
        
    def analyze_inventory_replenishment(self):
        """Analyze inventory and replenishment challenges"""
        print("Analyzing inventory and replenishment...")
        
        # Inventory turnover analysis
        turnover_stats = self.df['inventory_turnover'].describe()
        avg_turnover = turnover_stats['mean']
        
        # Lead time analysis
        lead_time_stats = self.df['replenishment_lead_time'].describe()
        avg_lead_time = lead_time_stats['mean']
        
        # Stockout risk analysis
        stockout_stats = self.df['stockout_risk_score'].describe()
        high_risk_items = len(self.df[self.df['stockout_risk_score'] > 70])
        
        # Safety stock analysis
        safety_stock_stats = self.df['safety_stock_level'].describe()
        
        # Category-wise turnover
        category_turnover = self.df.groupby('category')['inventory_turnover'].mean().sort_values(ascending=True)
        
        self.insights['inventory_replenishment'] = {
            'average_turnover': round(avg_turnover, 1),
            'average_lead_time': round(avg_lead_time, 1),
            'average_stockout_risk': round(stockout_stats['mean'], 1),
            'category_turnover': category_turnover.to_dict(),
            'challenges': {
                'slow_turning_categories': category_turnover[category_turnover < 3.0].to_dict(),
                'high_lead_time_items': len(self.df[self.df['replenishment_lead_time'] > 7]),
                'high_risk_items': high_risk_items,
                'excessive_safety_stock': len(self.df[self.df['safety_stock_level'] > self.df['quantity'] * 0.5])
            }
        }
        
    def analyze_pricing_promotion(self):
        """Analyze pricing and promotion challenges"""
        print("Analyzing pricing and promotion...")
        
        # Price elasticity analysis
        elasticity_stats = self.df['price_elasticity'].describe()
        avg_elasticity = elasticity_stats['mean']
        
        # Promotional lift analysis
        promo_lift_stats = self.df['promotional_lift'].describe()
        avg_promo_lift = promo_lift_stats['mean']
        
        # Margin impact analysis
        margin_stats = self.df['margin_impact'].describe()
        avg_margin_impact = margin_stats['mean']
        
        # Price sensitivity analysis
        price_sensitivity_stats = self.df['price_sensitivity_score'].describe()
        
        # Promotion effectiveness
        promo_effectiveness_stats = self.df['promotion_effectiveness'].describe()
        
        # Category-wise pricing analysis
        category_elasticity = self.df.groupby('category')['price_elasticity'].mean()
        category_promo_lift = self.df.groupby('category')['promotional_lift'].mean()
        
        self.insights['pricing_promotion'] = {
            'average_elasticity': round(avg_elasticity, 2),
            'average_promo_lift': round(avg_promo_lift, 1),
            'average_margin_impact': round(avg_margin_impact, 1),
            'average_price_sensitivity': round(price_sensitivity_stats['mean'], 1),
            'average_promo_effectiveness': round(promo_effectiveness_stats['mean'], 1),
            'category_elasticity': category_elasticity.to_dict(),
            'category_promo_lift': category_promo_lift.to_dict(),
            'challenges': {
                'high_elasticity_items': len(self.df[self.df['price_elasticity'] < -3.0]),
                'low_promo_lift_items': len(self.df[self.df['promotional_lift'] < 10]),
                'negative_margin_items': len(self.df[self.df['margin_impact'] < -10]),
                'ineffective_promotions': len(self.df[self.df['promotion_effectiveness'] < 50])
            }
        }
        
    def analyze_clustering_assortment(self):
        """Analyze store clustering and assortment challenges"""
        print("Analyzing clustering and assortment...")
        
        # Store cluster analysis
        cluster_distribution = self.df['store_cluster'].value_counts()
        
        # Assortment efficiency analysis
        assortment_stats = self.df['assortment_efficiency'].describe()
        avg_assortment_efficiency = assortment_stats['mean']
        
        # SKU performance analysis
        sku_performance_stats = self.df['sku_performance_score'].describe()
        
        # Category importance analysis
        category_importance_stats = self.df['category_importance_score'].describe()
        
        # Local market penetration
        market_penetration_stats = self.df['local_market_penetration'].describe()
        
        # Store region performance
        region_performance = self.df.groupby('store_region').agg({
            'assortment_efficiency': 'mean',
            'sku_performance_score': 'mean',
            'local_market_penetration': 'mean'
        }).round(1)
        
        self.insights['clustering_assortment'] = {
            'cluster_distribution': cluster_distribution.to_dict(),
            'average_assortment_efficiency': round(avg_assortment_efficiency, 1),
            'average_sku_performance': round(sku_performance_stats['mean'], 1),
            'average_category_importance': round(category_importance_stats['mean'], 1),
            'average_market_penetration': round(market_penetration_stats['mean'], 1),
            'region_performance': region_performance.to_dict(),
            'challenges': {
                'low_efficiency_stores': len(self.df[self.df['assortment_efficiency'] < 60]),
                'underperforming_skus': len(self.df[self.df['sku_performance_score'] < 50]),
                'low_penetration_markets': len(self.df[self.df['local_market_penetration'] < 60]),
                'cluster_imbalance': cluster_distribution.to_dict()
            }
        }
        
    def analyze_space_planning(self):
        """Analyze space planning and planogram challenges"""
        print("Analyzing space planning...")
        
        # Space utilization analysis
        space_stats = self.df['space_utilization'].describe()
        avg_space_utilization = space_stats['mean']
        
        # Planogram efficiency analysis
        planogram_stats = self.df['planogram_efficiency'].describe()
        avg_planogram_efficiency = planogram_stats['mean']
        
        # Customer flow analysis
        flow_stats = self.df['customer_flow_score'].describe()
        
        # Sales per square foot analysis
        sales_sqft_stats = self.df['sales_per_sqft'].describe()
        
        # Visual merchandising analysis
        visual_stats = self.df['visual_merchandising_score'].describe()
        
        # Category space allocation
        category_space = self.df.groupby('category')['category_space_allocation'].mean()
        
        # Store type performance
        store_type_performance = self.df.groupby('store_type').agg({
            'space_utilization': 'mean',
            'planogram_efficiency': 'mean',
            'sales_per_sqft': 'mean',
            'customer_flow_score': 'mean'
        }).round(1)
        
        self.insights['space_planning'] = {
            'average_space_utilization': round(avg_space_utilization, 1),
            'average_planogram_efficiency': round(avg_planogram_efficiency, 1),
            'average_customer_flow': round(flow_stats['mean'], 1),
            'average_sales_per_sqft': round(sales_sqft_stats['mean'], 1),
            'average_visual_merchandising': round(visual_stats['mean'], 1),
            'category_space_allocation': category_space.to_dict(),
            'store_type_performance': store_type_performance.to_dict(),
            'challenges': {
                'underutilized_stores': len(self.df[self.df['space_utilization'] < 70]),
                'inefficient_planograms': len(self.df[self.df['planogram_efficiency'] < 60]),
                'poor_flow_stores': len(self.df[self.df['customer_flow_score'] < 60]),
                'low_sales_density': len(self.df[self.df['sales_per_sqft'] < 800])
            }
        }
        
    def analyze_supplier_performance(self):
        """Analyze supplier performance challenges"""
        print("Analyzing supplier performance...")
        
        # Supplier performance analysis
        supplier_stats = self.df['supplier_performance_score'].describe()
        avg_supplier_performance = supplier_stats['mean']
        
        # Delivery reliability analysis
        delivery_stats = self.df['delivery_reliability'].describe()
        
        # Quality score analysis
        quality_stats = self.df['quality_score'].describe()
        
        # Cost efficiency analysis
        cost_efficiency_stats = self.df['supplier_cost_efficiency'].describe()
        
        # Innovation score analysis
        innovation_stats = self.df['supplier_innovation_score'].describe()
        
        # Risk score analysis
        risk_stats = self.df['supplier_risk_score'].describe()
        
        # Supplier distribution
        supplier_distribution = self.df['supplier_id'].value_counts().head(20)
        
        # Category-wise supplier performance
        category_supplier_performance = self.df.groupby('category').agg({
            'supplier_performance_score': 'mean',
            'delivery_reliability': 'mean',
            'quality_score': 'mean',
            'supplier_cost_efficiency': 'mean'
        }).round(1)
        
        self.insights['supplier_performance'] = {
            'average_supplier_performance': round(avg_supplier_performance, 1),
            'average_delivery_reliability': round(delivery_stats['mean'], 1),
            'average_quality_score': round(quality_stats['mean'], 1),
            'average_cost_efficiency': round(cost_efficiency_stats['mean'], 1),
            'average_innovation_score': round(innovation_stats['mean'], 1),
            'average_risk_score': round(risk_stats['mean'], 1),
            'top_suppliers': supplier_distribution.to_dict(),
            'category_supplier_performance': category_supplier_performance.to_dict(),
            'challenges': {
                'underperforming_suppliers': len(self.df[self.df['supplier_performance_score'] < 60]),
                'unreliable_deliveries': len(self.df[self.df['delivery_reliability'] < 70]),
                'quality_issues': len(self.df[self.df['quality_score'] < 70]),
                'high_cost_suppliers': len(self.df[self.df['supplier_cost_efficiency'] < 60]),
                'high_risk_suppliers': len(self.df[self.df['supplier_risk_score'] > 70])
            }
        }
        
    def generate_summary_insights(self):
        """Generate overall supply chain insights"""
        print("Generating summary insights...")
        
        # Overall performance metrics
        total_transactions = len(self.df)
        total_revenue = self.df['total_amount'].sum()
        avg_transaction_value = self.df['total_amount'].mean()
        
        # Key performance indicators
        kpis = {
            'total_transactions': total_transactions,
            'total_revenue': round(total_revenue, 2),
            'average_transaction_value': round(avg_transaction_value, 2),
            'forecast_accuracy': self.insights['demand_forecasting']['average_accuracy'],
            'inventory_turnover': self.insights['inventory_replenishment']['average_turnover'],
            'space_utilization': self.insights['space_planning']['average_space_utilization'],
            'supplier_performance': self.insights['supplier_performance']['average_supplier_performance']
        }
        
        # Critical challenges
        critical_challenges = {
            'demand_forecasting': {
                'low_accuracy_categories': len(self.insights['demand_forecasting']['challenges']['low_accuracy_categories']),
                'high_volatility_items': self.insights['demand_forecasting']['challenges']['high_volatility_items'],
                'weather_sensitive_items': self.insights['demand_forecasting']['challenges']['weather_sensitive_items']
            },
            'inventory_replenishment': {
                'slow_turning_categories': len(self.insights['inventory_replenishment']['challenges']['slow_turning_categories']),
                'high_lead_time_items': self.insights['inventory_replenishment']['challenges']['high_lead_time_items'],
                'high_risk_items': self.insights['inventory_replenishment']['challenges']['high_risk_items']
            },
            'pricing_promotion': {
                'high_elasticity_items': self.insights['pricing_promotion']['challenges']['high_elasticity_items'],
                'ineffective_promotions': self.insights['pricing_promotion']['challenges']['ineffective_promotions'],
                'negative_margin_items': self.insights['pricing_promotion']['challenges']['negative_margin_items']
            },
            'clustering_assortment': {
                'low_efficiency_stores': self.insights['clustering_assortment']['challenges']['low_efficiency_stores'],
                'underperforming_skus': self.insights['clustering_assortment']['challenges']['underperforming_skus'],
                'low_penetration_markets': self.insights['clustering_assortment']['challenges']['low_penetration_markets']
            },
            'space_planning': {
                'underutilized_stores': self.insights['space_planning']['challenges']['underutilized_stores'],
                'inefficient_planograms': self.insights['space_planning']['challenges']['inefficient_planograms'],
                'poor_flow_stores': self.insights['space_planning']['challenges']['poor_flow_stores']
            },
            'supplier_performance': {
                'underperforming_suppliers': self.insights['supplier_performance']['challenges']['underperforming_suppliers'],
                'unreliable_deliveries': self.insights['supplier_performance']['challenges']['unreliable_deliveries'],
                'quality_issues': self.insights['supplier_performance']['challenges']['quality_issues']
            }
        }
        
        self.insights['summary'] = {
            'kpis': kpis,
            'critical_challenges': critical_challenges,
            'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'dataset_size': f"{len(self.df):,} transactions"
        }
        
    def save_insights(self, output_path: str):
        """Save insights to JSON file"""
        with open(output_path, 'w') as f:
            json.dump(self.insights, f, indent=2)
        print(f"Insights saved to {output_path}")
        
    def run_analysis(self):
        """Run complete supply chain analysis"""
        print("Starting Supply Chain Data Analysis...")
        print("=" * 60)
        
        self.load_data()
        self.analyze_demand_forecasting()
        self.analyze_inventory_replenishment()
        self.analyze_pricing_promotion()
        self.analyze_clustering_assortment()
        self.analyze_space_planning()
        self.analyze_supplier_performance()
        self.generate_summary_insights()
        
        print("\nAnalysis Complete!")
        print("=" * 60)

def main():
    """Main function to run supply chain analysis"""
    dataset_path = "/Users/arghya.mukherjee/Downloads/cursor/sd/metadata/grocery_dataset.csv"
    output_path = "/Users/arghya.mukherjee/Downloads/cursor/sd/supply_chain/supply_chain_data_insights.json"
    
    analyzer = SupplyChainDataAnalyzer(dataset_path)
    analyzer.run_analysis()
    analyzer.save_insights(output_path)
    
    print(f"\nSupply chain insights generated and saved to: {output_path}")

if __name__ == "__main__":
    main()
