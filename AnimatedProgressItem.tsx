// src/AnimatedProgressItem.tsx
import React, { useEffect, useState } from 'react';
import { Progress } from "@/components/ui/progress";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip"; // TooltipProvider is in App.tsx
import { DashboardItem } from './data';

interface AnimatedProgressItemProps {
  item: DashboardItem;
  index: number; // For staggering animation within a category
}

const AnimatedProgressItem: React.FC<AnimatedProgressItemProps> = ({ item, index }) => {
  const [animatedValue, setAnimatedValue] = useState(0);

  useEffect(() => {
    // Stagger the animation start time slightly for each item
    const timer = setTimeout(() => {
      setAnimatedValue(item.percentage);
    }, 100 + index * 75); // Base delay + stagger per item

    return () => clearTimeout(timer);
  }, [item.percentage, index]);

  return (
    <li className="group">
      <Tooltip>
        <TooltipTrigger asChild>
          <div>
            <div className="flex justify-between items-center mb-1">
              <span className="text-sm font-medium text-slate-200 group-hover:text-sky-300 transition-colors duration-200">{item.name}</span>
              <span className="text-sm font-semibold text-pink-400">{item.percentage}%</span>
            </div>
            {/* The Progress component from shadcn/ui should animate changes to `value` due to its internal `transition-all` or `transition-transform` on the indicator */}
            <Progress value={animatedValue} className="h-3 [&>div]:bg-gradient-to-r [&>div]:from-pink-500 [&>div]:to-purple-600" />
          </div>
        </TooltipTrigger>
        <TooltipContent className="bg-slate-900 text-white border-slate-700">
          <p>{item.name}: {item.percentage}% Complete</p>
        </TooltipContent>
      </Tooltip>
    </li>
  );
};

export default AnimatedProgressItem;

