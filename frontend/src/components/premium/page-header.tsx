import { motion } from "motion/react";
import { type ReactNode } from "react";

export function PageHeader({ title, subtitle, icon, actions }: {
  title: string; subtitle?: string; icon?: ReactNode; actions?: ReactNode;
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: -8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="mb-8 flex items-start justify-between gap-4 flex-wrap"
    >
      <div className="flex items-start gap-4">
        {icon && (
          <div className="w-12 h-12 rounded-xl grid place-items-center glass"
            style={{ boxShadow: "0 0 30px oklch(0.68 0.19 245 / 0.3)" }}>
            {icon}
          </div>
        )}
        <div>
          <h1 className="text-3xl font-semibold tracking-tight">{title}</h1>
          {subtitle && <p className="text-muted-foreground mt-1 text-sm">{subtitle}</p>}
        </div>
      </div>
      {actions && <div className="flex items-center gap-2">{actions}</div>}
    </motion.div>
  );
}
